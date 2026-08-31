from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.inventory_forecasting.benchmark import MODELS, run_benchmarks, run_future_forecast
from src.inventory_forecasting.data import DEFAULT_DATASET, load_dataset, load_dataset_file
from src.inventory_forecasting.ui import execution_status, studio_model_catalog

st.set_page_config(page_title="Inventory Forecasting Studio", page_icon="📦", layout="wide")

st.title("📦 Inventory Forecasting Studio")
st.caption("Forecasting multi-SKU open source em Python — valide no histórico ou gere uma previsão futura")

with st.sidebar:
    st.header("Dados")
    data_source = st.radio(
        "Fonte do dataset",
        ["Dataset de demonstração", "Enviar meu CSV"],
        help="Use o dataset do projeto ou envie um CSV com o mesmo schema.",
    )
    horizon = st.number_input("Horizonte (dias)", min_value=1, max_value=14, value=7, step=1)
    uploaded_file = None
    if data_source == "Enviar meu CSV":
        uploaded_file = st.file_uploader("CSV de estoque", type=["csv"])
        st.caption("Máximo recomendado: 10 MB.")
    st.markdown("**Target:** `QUANTIDADE_ESTOQUE`")
    st.markdown("**Item ID:** `ID_PRODUTO`")
    st.markdown("**Timestamp:** `DATA_EVENTO`")
    st.markdown("**Campos:** `PRECO`, `FLAG_PROMOCAO`")

try:
    if data_source == "Enviar meu CSV":
        if uploaded_file is None:
            st.info("Envie um CSV para começar ou selecione o dataset de demonstração.")
            st.stop()
        if uploaded_file.size > 10 * 1024 * 1024:
            raise ValueError("Arquivo maior que 10 MB. Reduza o dataset para esta demonstração.")
        rows = load_dataset_file(io.BytesIO(uploaded_file.getvalue()))
        dataset_label = uploaded_file.name
    else:
        rows = load_dataset(DEFAULT_DATASET)
        dataset_label = str(DEFAULT_DATASET)
except Exception as exc:
    st.error(f"Não foi possível carregar o dataset: {exc}")
    st.stop()

frame = pd.DataFrame(rows)
counts = frame.groupby("ID_PRODUTO").size()

status_cols = st.columns(5)
status_cols[0].metric("Registros", len(frame))
status_cols[1].metric("SKUs", frame["ID_PRODUTO"].nunique())
status_cols[2].metric("Menor histórico/SKU", int(counts.min()))
status_cols[3].metric("Data inicial", str(frame["DATA_EVENTO"].min()))
status_cols[4].metric("Data final", str(frame["DATA_EVENTO"].max()))

st.caption(f"Dataset ativo: `{dataset_label}`")

tab_overview, tab_data, tab_validate, tab_future, tab_auto = st.tabs(
    ["Visão geral", "Dados & EDA", "🧪 Validação histórica", "🔮 Previsão futura", "AutoGluon"]
)

with tab_overview:
    st.subheader("Dois modos de uso")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🧪 Validar no passado")
        st.write(
            "Esconde os últimos dias já conhecidos, treina apenas com o passado e compara a previsão "
            "com os valores reais. É assim que calculamos erro e avaliamos se o método funciona."
        )
    with c2:
        st.markdown("### 🔮 Prever o futuro")
        st.write(
            "Usa todo o histórico disponível e gera datas posteriores à última observação. "
            "Essas linhas ainda não possuem valor real, portanto não têm métrica de erro até o futuro acontecer."
        )
    st.markdown("---")
    st.markdown(
        "Dataset → validação → backtest temporal → métricas → previsão futura → P10/P50/P90 → export"
    )
    st.info(
        "O SageMaker Canvas continua sendo a trilha oficial do desafio DIO. "
        "Este Studio é a implementação própria em Python criada como evolução adicional do projeto."
    )
    st.dataframe(pd.DataFrame(studio_model_catalog()), use_container_width=True, hide_index=True)

with tab_data:
    st.subheader("Dataset")
    st.dataframe(frame.head(100), use_container_width=True, hide_index=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Preço médio", f'{frame["PRECO"].mean():.2f}')
    col2.metric("Estoque médio", f'{frame["QUANTIDADE_ESTOQUE"].mean():.2f}')
    col3.metric("Promoções", f'{frame["FLAG_PROMOCAO"].mean() * 100:.2f}%')
    selected_sku = st.selectbox("SKU para visualizar", sorted(frame["ID_PRODUTO"].unique()), key="eda_sku")
    sku_frame = frame[frame["ID_PRODUTO"] == selected_sku].sort_values("DATA_EVENTO")
    fig = px.line(
        sku_frame,
        x="DATA_EVENTO",
        y="QUANTIDADE_ESTOQUE",
        markers=True,
        title=f"Histórico de estoque — SKU {selected_sku}",
    )
    st.plotly_chart(fig, use_container_width=True)

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = None
    st.session_state.predictions = None
if "future_predictions" not in st.session_state:
    st.session_state.future_predictions = None

with tab_validate:
    st.subheader("Validação histórica / holdout")
    st.write(
        f"O sistema esconde os últimos **{horizon} dias por SKU**, treina somente com datas anteriores e depois compara previsão × valor real."
    )
    st.caption(
        "As datas mostradas aqui pertencem ao dataset histórico. Elas não são uma previsão futura; são um teste controlado de desempenho."
    )

    if counts.min() <= int(horizon):
        st.error("O menor histórico por SKU precisa ter mais observações do que o horizonte escolhido.")
    elif st.button("Executar validação histórica", type="primary"):
        try:
            leaderboard, predictions = run_benchmarks(rows, horizon=int(horizon))
            st.session_state.leaderboard = leaderboard
            st.session_state.predictions = predictions
        except Exception as exc:
            st.error(f"Não foi possível executar a validação: {exc}")

    if st.session_state.leaderboard:
        leaderboard_df = pd.DataFrame(st.session_state.leaderboard)
        display = leaderboard_df.copy()
        for metric in ["MAE", "RMSE", "WAPE", "MAPE", "MACRO_MASE", "WQL"]:
            display[metric] = display[metric].map(lambda value: f"{value:.6f}")
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.caption("Ranking primário por WAPE; RMSE desempata. `MACRO_MASE` é calculado por SKU e depois promediado.")

        pred = pd.DataFrame(st.session_state.predictions)
        model = st.selectbox("Modelo validado", sorted(pred["model"].unique()), key="validation_model")
        sku = st.selectbox("SKU", sorted(pred["ID_PRODUTO"].unique()), key="validation_sku")
        view = pred[(pred["model"] == model) & (pred["ID_PRODUTO"] == sku)].copy()
        melted = view.melt(
            id_vars=["DATA_EVENTO", "actual"],
            value_vars=["P10", "P50", "P90"],
            var_name="quantile",
            value_name="forecast",
        )
        fig = px.line(melted, x="DATA_EVENTO", y="forecast", color="quantile", markers=True, title=f"Backtest — {model} — SKU {sku}")
        fig.add_scatter(x=view["DATA_EVENTO"], y=view["actual"], name="Real", mode="lines+markers")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button(
            "Baixar resultados do backtest",
            pred.to_csv(index=False).encode("utf-8"),
            "historical_validation_predictions.csv",
            "text/csv",
        )

with tab_future:
    st.subheader("Previsão para datas futuras")
    st.write(
        "Aqui o sistema usa **todo o histórico disponível**. A primeira data prevista é o dia seguinte à última observação de cada SKU."
    )
    st.warning(
        "Como essas datas estão depois do dataset, ainda não existe `valor real` para medir erro. "
        "P10/P50/P90 representam cenários de incerteza dos baselines, não garantia de estoque futuro."
    )

    future_model = st.selectbox("Modelo para previsão futura", list(MODELS.keys()), index=0)
    if future_model == "SeasonalNaive7" and counts.min() < 7:
        st.error("SeasonalNaive7 exige pelo menos 7 observações por SKU.")
    elif counts.min() < 2:
        st.error("São necessárias pelo menos 2 observações por SKU para previsão futura.")
    elif st.button("Gerar previsão futura", type="primary"):
        try:
            st.session_state.future_predictions = run_future_forecast(
                rows,
                horizon=int(horizon),
                model_name=future_model,
            )
        except Exception as exc:
            st.error(f"Não foi possível gerar a previsão: {exc}")

    if st.session_state.future_predictions:
        future_df = pd.DataFrame(st.session_state.future_predictions)
        future_sku = st.selectbox("SKU previsto", sorted(future_df["ID_PRODUTO"].unique()), key="future_sku")
        view = future_df[future_df["ID_PRODUTO"] == future_sku].copy()
        melted = view.melt(
            id_vars=["DATA_EVENTO"],
            value_vars=["P10", "P50", "P90"],
            var_name="quantile",
            value_name="forecast",
        )
        fig = px.line(
            melted,
            x="DATA_EVENTO",
            y="forecast",
            color="quantile",
            markers=True,
            title=f"Previsão futura — {view['model'].iloc[0]} — SKU {future_sku}",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar previsão futura CSV",
            future_df.to_csv(index=False).encode("utf-8"),
            "future_inventory_forecast.csv",
            "text/csv",
        )

with tab_auto:
    st.subheader("AutoGluon TimeSeries — experimento avançado")
    auto_status = execution_status("results/autogluon/leaderboard.csv")
    st.metric("Status de artefatos versionados", auto_status)
    st.write(
        "AutoGluon foi usado na análise científica do projeto e possui resultados reproduzíveis, "
        "mas não é carregado no clique do app público para manter a experiência leve e barata."
    )
    st.code(
        "pip install -r requirements-ml.txt\n"
        "python scripts/train_autogluon.py --time-limit 180 --presets medium_quality\n"
        "python scripts/train_autogluon_multifold.py --time-limit 180 --presets medium_quality",
        language="bash",
    )

    validated = Path("results/validated")
    summary_path = validated / "autogluon_multifold_summary.csv"
    stability_path = validated / "model_stability.csv"
    horizon_path = validated / "horizon_calibration.csv"
    sku_path = validated / "sku_metrics.csv"

    if summary_path.exists() and stability_path.exists():
        summary = pd.read_csv(summary_path).iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("WAPE médio — 3 folds", f'{summary["WAPE_mean"]:.3f}')
        c2.metric("WQL médio — 3 folds", f'{summary["WQL_mean"]:.3f}')
        c3.metric("Coverage P10–P90", f'{summary["P10_P90_COVERAGE_mean"] * 100:.1f}%')
        c4.metric("Vitórias externas ensemble", f'{int(summary["weighted_ensemble_external_wins"])}/3')
        st.dataframe(pd.read_csv(stability_path), use_container_width=True, hide_index=True)

        if horizon_path.exists():
            st.markdown("#### Calibração por horizonte")
            st.dataframe(pd.read_csv(horizon_path), use_container_width=True, hide_index=True)
        if sku_path.exists():
            st.markdown("#### Diagnóstico por SKU")
            st.dataframe(pd.read_csv(sku_path), use_container_width=True, hide_index=True)
