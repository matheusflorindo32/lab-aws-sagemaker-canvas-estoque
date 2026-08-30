# 📦 Inventory Forecasting Studio

### DIO SageMaker Canvas Challenge + implementação open source reproduzível com AutoGluon TimeSeries

[![DIO](https://img.shields.io/badge/DIO-Project%20Lab-6C63FF)](https://www.dio.me/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![AutoGluon](https://img.shields.io/badge/AutoGluon-TimeSeries%201.6.1-4B8BBE)](https://auto.gluon.ai/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Forecasting%20Studio-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Dataset validation](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/dataset-validation.yml/badge.svg?branch=feat/professional-ml-portfolio)](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/dataset-validation.yml)
[![Python forecasting](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/python-forecasting.yml/badge.svg?branch=feat/professional-ml-portfolio)](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/python-forecasting.yml)
[![Security](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/security.yml/badge.svg?branch=feat/professional-ml-portfolio)](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/security.yml)

> Forecasting multi-SKU com validação temporal rolling-origin, baselines, AutoML probabilístico, P10/P50/P90, calibração, diagnóstico por SKU, Streamlit, CI e evidências reproduzíveis.

---

## Estado do projeto

Este repositório preserva duas trilhas distintas:

| Trilha | Status | Objetivo |
|---|---|---|
| ☁️ SageMaker Canvas | ⏳ **NÃO EXECUTADA** | cumprir o fluxo original específico da DIO |
| 🐍 Python / AutoGluon / Streamlit | ✅ **EXECUTADA** | implementação open source reproduzível e auditável |

Nenhuma métrica Python é apresentada como resultado AWS.

### O que este projeto é hoje

- demonstrador funcional de forecasting multi-SKU;
- projeto educacional/portfólio com experimentação real;
- implementação reproducível com CI;
- **não** é plataforma de inventory optimization production-ready.

---

# Problema

O desafio original prevê `QUANTIDADE_ESTOQUE` por SKU. Esse target foi mantido por aderência pedagógica.

> **Estoque observado não é demanda.**

Em uma solução corporativa, o fluxo mais apropriado tende a ser:

`demanda/saídas → forecast → lead time → safety stock → reorder point → recomendação de reposição → estoque projetado`

Neste dataset, reposições/resets do estoque são intervenções operacionais e aumentam a dificuldade de interpretação.

---

# Dataset

Arquivo principal:

`datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv`

| Propriedade | Resultado validado |
|---|---:|
| Registros | 1.000 |
| SKUs | 25 |
| Observações/SKU | 40 |
| Frequência | diária |
| Intervalo | 2023-12-31 a 2024-02-08 |
| Missing | 0 |
| Duplicatas exatas | 0 |
| Duplicatas SKU+data | 0 |
| Pontos diários ausentes | 0 |
| Linhas inválidas | 0 |

Dataset SHA-256 do experimento P1:

`fe8ffe48cc34cd8540ecba10984066fe503b0bb5ca9d55f9280d5b1960649031`

---

# Protocolo experimental

## Holdout final

- treino: 33 observações/SKU;
- teste: 7 observações/SKU;
- 25 × 7 = 175 observações externas.

## Robustez temporal P1

Foram adicionados **3 folds rolling-origin / expanding-window**, com testes externos de 7 dias **não sobrepostos**:

| Fold | Treino/SKU | Teste/SKU |
|---:|---:|---:|
| 1 | 19 | 7 |
| 2 | 26 | 7 |
| 3 | 33 | 7 |

A seleção do modelo AutoGluon acontece pela validação interna; o teste externo não escolhe o modelo.

---

# Benchmarks

Baselines:

- `Naive`;
- `Drift`;
- `SeasonalNaive7`.

O Naive foi o melhor baseline por WAPE nos três folds.

| Modelo | WAPE médio | RMSE médio | MACRO_MASE médio | WQL médio |
|---|---:|---:|---:|---:|
| **Naive** | **0.739365** | **45.785757** | **2.588005** | **0.647723** |
| Drift | 0.809554 | 52.004579 | 2.853404 | 0.690580 |
| SeasonalNaive7 | 0.874120 | 49.939643 | 3.010651 | 0.818905 |

`MACRO_MASE` = MASE calculado por SKU e depois promediado.

---

# AutoGluon TimeSeries

Configuração executada:

```text
AutoGluon TimeSeries: 1.6.1
Python: 3.12.14
prediction_length: 7
freq: D
eval_metric: WQL
quantiles: [0.1, 0.5, 0.9]
known covariates: PRECO, FLAG_PROMOCAO
preset: medium_quality
random_seed: 123
```

Famílias treinadas no holdout final:

`SeasonalNaive` · `RecursiveTabular` · `DirectTabular` · `ETS` · `Theta` · `Chronos2` · `Toto2` · `WeightedEnsemble`

## Resultados externos por fold

| Fold | Selecionado internamente | Vencedor externo | Rank externo do ensemble | WAPE do ensemble | WQL do ensemble |
|---:|---|---|---:|---:|---:|
| 1 | WeightedEnsemble | **Chronos2** | **3** | 0.700500 | 0.424289 |
| 2 | WeightedEnsemble | **WeightedEnsemble** | **1** | 0.441683 | 0.262329 |
| 3 | WeightedEnsemble | **WeightedEnsemble** | **1** | 0.358348 | 0.223493 |

### Interpretação de estabilidade

- **selection stability: `stable`** — WeightedEnsemble foi escolhido pela validação interna em 3/3 folds;
- **external test stability: `unstable`** — venceu 2/3 testes, mas no fold 1 caiu para terceiro e teve WQL ~27,16% pior que o Chronos2.

Portanto, o projeto **não afirma que WeightedEnsemble é universalmente o melhor modelo**.

## Resultado agregado em 3 folds

| Métrica | Média | Mediana | Desvio-padrão |
|---|---:|---:|---:|
| MAE | 26.145005 | 21.960458 | 7.857459 |
| RMSE | 31.917570 | 28.859860 | 7.398349 |
| WAPE | 0.500177 | 0.441683 | 0.178418 |
| WQL | 0.303370 | 0.262329 | 0.106504 |

### AutoGluon vs melhor baseline

Nos mesmos três folds, comparando o modelo selecionado pelo AutoGluon ao Naive:

- WAPE médio: **32,35% menor**;
- RMSE médio: **30,29% menor**;
- WQL médio: **53,16% menor**.

Isso é evidência positiva neste dataset, não garantia de desempenho de produção.

---

# Forecast probabilístico — P10/P50/P90

A calibração foi medida, não presumida.

| Diagnóstico agregado | Resultado |
|---|---:|
| `y <= P10` | 20.95% |
| `y <= P50` | 51.05% |
| `y <= P90` | 88.19% |
| Coverage P10–P90 | **67.24%** |
| Coverage nominal esperado | ~80% |
| Largura média P10–P90 | 68.52 |
| Quantile crossings | **0** |

Os intervalos apresentam **subcoverage**. Quantis nativos do modelo não significam calibração perfeita.

A análise por horizonte h=1..7 e por SKU está em [`results/validated/`](results/validated/).

---

# Diagnóstico por SKU

Cinco menores MAEs médios nos três folds:

`1011`, `1013`, `1005`, `1022`, `1024`.

Cinco maiores:

`1006`, `1008`, `1004`, `1002`, `1015`.

Essas diferenças são descritivas; o histórico curto não permite conclusão causal.

---

# Holdout final

No fold final, WeightedEnsemble teve:

| Métrica | Valor |
|---|---:|
| MAE | 21.265417 |
| RMSE | 26.538214 |
| WAPE | 0.358348 |
| MAPE | 1.472072 |
| WQL | 0.223493 |

Feature importance:

- `PRECO`: 0.000169;
- `FLAG_PROMOCAO`: -0.000625.

Os valores ficaram praticamente nulos neste experimento e não são interpretados causalmente.

---

# Evidências e reprodutibilidade

Resultados P1 pequenos e auditáveis são preservados em:

[`results/validated/`](results/validated/)

Incluindo:

- métricas por fold;
- summary agregado;
- estabilidade dos modelos;
- calibração por horizonte;
- métricas por SKU;
- manifesto com dataset hash e proveniência do artifact;
- summary dos benchmarks.

### Executar

```bash
python -m venv .venv
pip install -r requirements-ml.txt
python scripts/validate_dataset.py
python scripts/run_benchmarks.py
python scripts/train_autogluon.py --time-limit 180 --presets medium_quality
python scripts/train_autogluon_multifold.py --time-limit 180 --presets medium_quality
```

### Streamlit

```bash
pip install -r requirements-app.txt
streamlit run app.py
```

O Studio exibe dataset/EDA, benchmarks, leaderboard, estabilidade externa, calibração por horizonte, diagnóstico por SKU e forecasts.

---

# Qualidade e CI

A suíte atual possui **23 testes**, cobrindo:

- qualidade do dataset;
- duplicata SKU+data;
- métricas de ponto;
- WQL/pinball;
- MACRO_MASE;
- rolling-origin e ausência de leakage temporal;
- benchmarks multifold;
- configuração AutoGluon;
- separação entre seleção interna e estabilidade externa;
- contratos de UI;
- secret scanner.

Workflows incluem:

- Dataset validation;
- Python forecasting;
- AutoGluon experiment;
- Streamlit smoke test;
- secret scan;
- dependency audit com `pip-audit`.

GitHub Actions oficiais estão pinadas por commit SHA e workflows usam `contents: read`.

## Risco de dependência conhecido

`lightning 2.6.5` possui `PYSEC-2026-3624 / CVE-2026-58659`. Em 30/08/2026 ainda não havia release PyPI corrigida. O fluxo atual não aceita checkpoints não confiáveis nem chama o caminho vulnerável com conteúdo de usuário; o finding permanece como exceção temporária, estreita e documentada em [`SECURITY.md`](SECURITY.md).

---

# ☁️ SageMaker Canvas / DIO

## Status: **NÃO EXECUTADO**

Configuração planejada:

| Parâmetro | Valor |
|---|---|
| Tipo | Time Series Forecasting |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Frequência | Daily |
| Horizonte | 7 dias |
| Covariáveis | `PRECO`, `FLAG_PROMOCAO` |

O guia de execução está em [`docs/04-configuracao-sagemaker-canvas.md`](docs/04-configuracao-sagemaker-canvas.md).

O gate FinOps atualizado está em [`docs/10-custos-aws.md`](docs/10-custos-aws.md).

**Nenhum recurso AWS pago deve ser iniciado sem autorização explícita.**

---

# Limitações

- 40 observações por SKU continuam sendo pouco histórico;
- primeiro fold possui somente 19 pontos de treino;
- três folds melhoram a evidência, mas não provam generalização corporativa;
- dataset educacional;
- estoque é influenciado por reposição/intervenção;
- não há série explícita de demanda/vendas;
- covariáveis futuras precisam ser conhecidas no momento da previsão;
- P10–P90 está subcalibrado;
- estabilidade externa do ensemble é limitada;
- não existem autenticação, banco, serving, monitoramento de produção ou política automática de reposição.

---

# Próxima evolução correta

Depois de concluir a trilha Canvas/DIO, um MVP real deveria mudar o foco de “mais modelos” para **decisão de estoque**:

`vendas/demanda + estoque atual + lead time → forecast → safety stock → reorder point → quantidade recomendada`

Sem Kubernetes, Kafka, feature store ou microservices antes de existir necessidade operacional mensurável.
