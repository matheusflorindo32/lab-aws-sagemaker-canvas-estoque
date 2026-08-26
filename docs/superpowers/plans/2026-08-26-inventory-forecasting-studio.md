# Inventory Forecasting Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transformar o Lab DIO em um Inventory Forecasting Studio open source executado em Python, preservando o SageMaker Canvas como trilha original documentada e sem apresentar resultados não executados como reais.

**Architecture:** O projeto terá uma camada de dados/validação existente, um pipeline reproduzível de forecasting multi-SKU com holdout temporal de 7 dias, benchmarks leves e uma integração opcional com AutoGluon TimeSeries. Uma aplicação Streamlit consumirá os mesmos artefatos e funções do pipeline para oferecer experiência visual semelhante a um estúdio AutoML. Resultados versionados só serão produzidos após execução real e verificável.

**Tech Stack:** Python 3.12, pandas, numpy, scikit-learn, statsmodels, AutoGluon TimeSeries, Streamlit, Plotly, GitHub Actions.

**Spec:** Solicitação aprovada no PR #1: implementar trilha open source em Python com AutoGluon TimeSeries, Streamlit, benchmarks, validação temporal, leaderboard, métricas, P10/P50/P90, covariáveis, gráficos, exports, testes, CI e documentação profissional.

## Global Constraints

- Dataset principal: `datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv`.
- Target: `QUANTIDADE_ESTOQUE`.
- Item ID: `ID_PRODUTO`.
- Timestamp: `DATA_EVENTO`.
- Horizonte: 7 dias.
- Covariáveis: `PRECO`, `FLAG_PROMOCAO` quando conhecidas no horizonte.
- Não alterar os CSVs originais da DIO.
- Não registrar como reais métricas, forecasts, quantis, feature importance ou custos que não tenham sido executados e verificados.
- SageMaker Canvas permanece como trilha original da DIO e deve ser marcado como não executado nesta implementação.
- CI não deve executar treinamento pesado de AutoGluon; deve executar testes, validação de dados e smoke tests leves.

---

### Task 1: Forecasting core e métricas

**Files:**
- Create: `src/inventory_forecasting/__init__.py`
- Create: `src/inventory_forecasting/data.py`
- Create: `src/inventory_forecasting/metrics.py`
- Create: `src/inventory_forecasting/backtest.py`
- Test: `tests/test_forecasting_core.py`

- [ ] Implementar carregamento padronizado e split temporal de 7 dias por SKU.
- [ ] Implementar MAE, RMSE, WAPE, MAPE seguro, MASE e weighted quantile loss.
- [ ] Testar ausência de leakage temporal e cálculo das métricas em exemplos pequenos conhecidos.

### Task 2: Benchmarks reproduzíveis

**Files:**
- Create: `src/inventory_forecasting/baselines.py`
- Create: `src/inventory_forecasting/benchmark.py`
- Test: `tests/test_benchmarks.py`

- [ ] Implementar Naive, Seasonal Naive e drift/trend como benchmarks sem dependências pesadas.
- [ ] Gerar previsões de 7 dias no holdout e leaderboard comparável pelas mesmas métricas.
- [ ] Selecionar o melhor benchmark apenas por métricas calculadas no holdout.

### Task 3: Integração AutoGluon TimeSeries

**Files:**
- Create: `src/inventory_forecasting/autogluon_runner.py`
- Create: `scripts/train_autogluon.py`
- Create: `requirements-ml.txt`
- Test: `tests/test_autogluon_contract.py`

- [ ] Criar adapter para `TimeSeriesDataFrame` com item/timestamp/target corretos.
- [ ] Configurar `prediction_length=7`, quantis 0.1/0.5/0.9 e covariáveis conhecidas quando fornecidas.
- [ ] Exportar leaderboard, métricas e forecasts reais quando AutoGluon estiver instalado.
- [ ] Falhar de forma explícita e útil quando a dependência não estiver instalada; nunca simular resultados.

### Task 4: Inventory Forecasting Studio em Streamlit

**Files:**
- Create: `app.py`
- Create: `src/inventory_forecasting/ui.py`
- Create: `requirements-app.txt`
- Test: `tests/test_ui_contract.py`

- [ ] Criar fluxo Dataset → Validação → EDA → Configuração → Benchmarks/AutoML → Leaderboard → Forecast → Export.
- [ ] Exibir claramente status `Executado`, `Não executado` e `Opcional AutoGluon`.
- [ ] Exibir gráficos e tabelas sem fabricar outputs ausentes.

### Task 5: Artefatos reproduzíveis e resultados reais

**Files:**
- Create: `scripts/run_benchmarks.py`
- Create/Update: `results/metrics/benchmark_metrics.csv`
- Create/Update: `results/predictions/benchmark_holdout_predictions.csv`
- Create/Update: `results/exports/benchmark_leaderboard.csv`

- [ ] Executar benchmarks leves no dataset real.
- [ ] Registrar somente outputs reproduzidos pela execução.
- [ ] Validar que todas as linhas do holdout pertencem aos últimos 7 dias de cada SKU.

### Task 6: CI e segurança

**Files:**
- Modify: `.github/workflows/dataset-validation.yml`
- Create: `.github/workflows/python-forecasting.yml`

- [ ] Compilar scripts e pacote.
- [ ] Executar unit tests.
- [ ] Executar smoke benchmark leve e verificar determinismo estrutural.
- [ ] Manter `contents: read` e sem secrets AWS.

### Task 7: Documentação e PR

**Files:**
- Modify: `README.md`
- Create: `docs/05-implementacao-python.md`
- Create: `docs/07-resultados-python.md`
- Create: `docs/08-inventory-forecasting-studio.md`
- Modify: `CHANGELOG.md`

- [ ] Separar claramente `Trilha DIO — SageMaker Canvas` e `Trilha executada — Python open source`.
- [ ] Documentar arquitetura, comandos de execução, métricas reais, limitações e próximos passos.
- [ ] Atualizar PR #1 com evidências de testes e workflows.

### Task 8: Auditoria final

- [ ] Verificar árvore final, diff, CI, segurança e consistência entre README e arquivos.
- [ ] Confirmar que nenhum resultado AutoGluon foi versionado sem execução real.
- [ ] Não fazer merge enquanto houver pendência técnica relevante ou CI vermelho.
