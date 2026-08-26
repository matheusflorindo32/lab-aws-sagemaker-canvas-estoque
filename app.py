from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.inventory_forecasting.benchmark import run_benchmarks
from src.inventory_forecasting.data import DEFAULT_DATASET, load_dataset
from src.inventory_forecasting.ui import execution_status, studio_model_catalog

st.set_page_config(page_title="Inventory Forecasting Studio", page_icon="📦", layout="wide")

st.title("📦 Inventory Forecasting Studio")
st.caption("Forecasting multi-SKU open source em Python — trilha executada do Lab DIO")

with st.sidebar:
    st.header("Configuração")
    dataset_path = st.text_input("Dataset", value=str(DEFAULT_DATASET))
    horizon = st.number_input("Horizonte", min_value=1, max_value=14, value=7, step=1)
    st.markdown("**Target:** `QUANTIDADE_ESTOQUE`")
    st.markdown("**Item ID:** `ID_PRODUTO`")
    st.markdown("**Timestamp:** `DATA_EVENTO`")
    st.markdown("**Covariáveis:** `PRECO`, `FLAG_PROMOCAO`")

try:
    rows = load_dataset(dataset_path)
except Exception as exc:
    st.error(f"Não foi possível carregar o dataset: {exc}")
    st.stop()

frame = pd.DataFrame(rows)

status_cols = st.columns(4)
status_cols[0].metric("Registros", len(frame))
status_cols[1].metric("SKUs", frame["ID_PRODUTO"].nunique())
status_cols[2].metric("Data inicial", str(frame["DATA_EVENTO"].min()))
status_cols[3].metric("Data final", str(frame["DATA_EVENTO"].max()))

tab_overview, tab_data, tab_bench, tab_auto, tab_forecast = st.tabs(
    ["Visão geral", "Dados & EDA", "Benchmarks", "AutoGluon", "Forecast"]
)

with tab_overview:
    st.subheader("Arquitetura executada")
    st.markdown(
        "Dataset → validação → holdout temporal → benchmarks → métricas → "
        "AutoGluon opcional → leaderboard → forecast probabilístico → export"
    )
    st.info(
        "O SageMaker Canvas permanece documentado como trilha original da DIO. "
        "Esta aplicação representa a trilha open source realmente executável no repositório."
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
    fig = px.line(sku_frame, x="DATA_EVENTO", y="QUANTIDADE_ESTOQUE", markers=True, title=f"Estoque — SKU {selected_sku}")
    st.plotly_chart(fig, use_container_width=True)

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = None
    st.session_state.predictions = None

with tab_bench:
    st.subheader("Backtest temporal")
    st.write(f"Os últimos **{horizon} dias por SKU** formam o holdout; nenhuma linha futura entra no treino.")
    if st.button("Executar benchmarks", type="primary"):
        leaderboard, predictions = run_benchmarks(rows, horizon=int(horizon))
        st.session_state.leaderboard = leaderboard
        st.session_state.predictions = predictions

    if st.session_state.leaderboard:
        leaderboard_df = pd.DataFrame(st.session_state.leaderboard)
        display = leaderboard_df.copy()
        for metric in ["MAE", "RMSE", "WAPE", "MAPE", "MASE", "WQL"]:
            display[metric] = display[metric].map(lambda value: f"{value:.6f}")
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.caption("Ranking primário por WAPE; RMSE é critério de desempate.")
        st.download_button(
            "Baixar leaderboard CSV",
            leaderboard_df.to_csv(index=False).encode("utf-8"),
            "benchmark_leaderboard.csv",
            "text/csv",
        )
    else:
        st.warning("Benchmarks ainda não executados nesta sessão.")

with tab_auto:
    st.subheader("AutoGluon TimeSeries")
    auto_status = execution_status("results/autogluon/leaderboard.csv")
    st.metric("Status de artefatos versionados", auto_status)
    st.code(
        "pip install -r requirements-ml.txt\n"
        "python scripts/train_autogluon.py --time-limit 300 --presets medium_quality",
        language="bash",
    )
    st.markdown(
        "Configuração: `prediction_length=7`, `freq='D'`, `eval_metric='WQL'`, "
        "quantis `0.1/0.5/0.9`, covariáveis conhecidas `PRECO` e `FLAG_PROMOCAO`."
    )
    st.warning(
        "Resultados AutoGluon só aparecem aqui depois de uma execução real. "
        "O Studio nunca gera valores simulados para preencher esta seção."
    )
    auto_leaderboard = Path("results/autogluon/leaderboard.csv")
    if auto_leaderboard.exists():
        st.dataframe(pd.read_csv(auto_leaderboard), use_container_width=True, hide_index=True)

with tab_forecast:
    st.subheader("Holdout forecast")
    if not st.session_state.predictions:
        st.warning("Execute os benchmarks primeiro.")
    else:
        pred = pd.DataFrame(st.session_state.predictions)
        model = st.selectbox("Modelo", sorted(pred["model"].unique()))
        sku = st.selectbox("SKU", sorted(pred["ID_PRODUTO"].unique()), key="forecast_sku")
        view = pred[(pred["model"] == model) & (pred["ID_PRODUTO"] == sku)].copy()
        melted = view.melt(
            id_vars=["DATA_EVENTO", "actual"],
            value_vars=["P10", "P50", "P90"],
            var_name="quantile",
            value_name="forecast",
        )
        fig = px.line(melted, x="DATA_EVENTO", y="forecast", color="quantile", markers=True, title=f"{model} — SKU {sku}")
        fig.add_scatter(x=view["DATA_EVENTO"], y=view["actual"], name="Actual", mode="lines+markers")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.caption(
            "Nos benchmarks leves, P10/P50/P90 são derivados empiricamente das inovações históricas. "
            "AutoGluon, quando executado, produz quantis probabilísticos nativos do modelo."
        )
        st.download_button(
            "Baixar forecast CSV",
            view.to_csv(index=False).encode("utf-8"),
            f"forecast_{model}_{sku}.csv",
            "text/csv",
        )
