# ✨ Previsão de Estoque Inteligente — DIO + AWS SageMaker Canvas + Python

> **Desafio oficial DIO evoluído para um projeto completo de forecasting, com duas trilhas complementares:** a execução visual no **Amazon SageMaker Canvas** e uma implementação própria, reproduzível e auditável em **Python + AutoGluon + Streamlit**.

[![DIO](https://img.shields.io/badge/DIO-Project%20Challenge-6C63FF)](https://www.dio.me/)
[![AWS](https://img.shields.io/badge/AWS-SageMaker%20Canvas-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/sagemaker/ai/canvas/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![AutoGluon](https://img.shields.io/badge/AutoGluon-TimeSeries-4B8BBE)](https://auto.gluon.ai/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Forecasting%20Studio-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

---

## 💎 Executive Project Board

| Dimensão | Status | Entrega |
|---|---|---|
| 🎯 Desafio DIO | **Preparado** | fluxo oficial reconstruído e documentado |
| ☁️ SageMaker Canvas | **Execução real pendente** | import → build → métricas → forecast → export |
| 🐍 Versão própria em Python | **Executada** | forecasting completo e reproduzível |
| 📊 Validação temporal | **Executada** | 3 folds rolling-origin / expanding-window |
| 🤖 AutoML | **Executado** | AutoGluon TimeSeries 1.6.1 |
| 🎯 Forecast probabilístico | **Executado** | P10 / P50 / P90 + calibration |
| 🖥️ Dashboard | **Executado** | Streamlit Inventory Forecasting Studio |
| 🧪 Qualidade | **25 testes** | dataset, métricas, folds, segurança e readiness |
| 🔐 Segurança | **Hardened** | secret scan, pip-audit e Actions pinadas por SHA |
| 📦 Evidências | **Estruturadas** | resultados, manifestos, checklist e matriz DIO |
| 🚀 Submissão DIO | **READY AFTER CANVAS** | falta apenas a evidência real da execução AWS |

---

# 🎯 Sobre o desafio DIO

Este projeto nasceu do desafio **“Previsão de Estoque Inteligente na AWS com SageMaker Canvas”** da Digital Innovation One.

O fluxo esperado pela atividade é:

1. escolher um dataset;
2. importar os dados no Amazon SageMaker Canvas;
3. configurar o problema de previsão;
4. treinar o modelo;
5. analisar métricas e importância das características;
6. gerar previsões;
7. exportar os resultados;
8. registrar conclusões;
9. enviar o link do repositório na DIO.

---

# 🚀 Como o projeto foi evoluído

Em vez de apenas reproduzir o laboratório visual, o projeto foi **ampliado e profissionalizado**.

A proposta passou a ter duas implementações do mesmo problema:

```text
                  DATASET DE ESTOQUE
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
   ☁️ AWS SAGEMAKER CANVAS      🐍 PYTHON STACK
       trilha oficial DIO       implementação própria
             │                       │
      Time Series Forecast       validação de dados
             │                       │
        model build             rolling-origin
             │                       │
       metrics / impact         baselines + AutoGluon
             │                       │
           forecast             P10 / P50 / P90
             │                       │
            export              Streamlit Studio
             └───────────┬───────────┘
                         ▼
                ANÁLISE COMPARATIVA
```

### O que foi modificado em relação ao projeto original

O desafio original foi preservado, mas recebeu uma camada adicional de engenharia e ciência de dados:

- validação automatizada do dataset;
- checagem de cardinalidade e duplicatas `SKU + data`;
- análise exploratória;
- baselines `Naive`, `Drift` e `SeasonalNaive7`;
- backtest temporal;
- 3 folds rolling-origin / expanding-window;
- AutoGluon TimeSeries;
- MAE, RMSE, WAPE, MAPE, WQL e `MACRO_MASE`;
- forecast probabilístico P10/P50/P90;
- avaliação de coverage e calibração;
- diagnóstico por SKU e horizonte;
- Streamlit para exploração visual;
- testes automatizados;
- GitHub Actions;
- dependency audit e secret scanning;
- artifacts e manifestos reproduzíveis;
- readiness checker específico para submissão DIO.

A trilha Python **não substitui** o SageMaker Canvas. Ela demonstra como o mesmo problema pode ser implementado de forma programática, reproduzível e auditável.

---

# 📁 Dataset

Arquivo principal:

```text
datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv
```

| Propriedade | Resultado |
|---|---:|
| Registros | **1.000** |
| SKUs | **25** |
| Observações por SKU | **40** |
| Frequência | diária |
| Período | 2023-12-31 → 2024-02-08 |
| Missing | **0** |
| Duplicatas exatas | **0** |
| Duplicatas SKU+data | **0** |
| Pontos diários ausentes | **0** |
| Linhas inválidas | **0** |

### Schema

| Campo | Papel |
|---|---|
| `ID_PRODUTO` | Item ID |
| `DATA_EVENTO` | timestamp |
| `PRECO` | variável adicional |
| `FLAG_PROMOCAO` | variável adicional |
| `QUANTIDADE_ESTOQUE` | target |

---

# ☁️ Trilha oficial — Amazon SageMaker Canvas

Configuração preparada para a execução real:

| Parâmetro | Valor planejado |
|---|---|
| Problem type | Time Series Forecasting |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Forecast length | **7 dias** |
| Frequência | diária |
| Colunas adicionais | `PRECO`, `FLAG_PROMOCAO` quando suportadas pelo fluxo real |

### Status

**SageMaker Canvas ainda não foi executado neste repositório.**

Isso é intencionalmente declarado para manter a rastreabilidade: nenhum resultado Python é apresentado como resultado AWS.

Após a execução real serão adicionadas as evidências de:

- import do dataset;
- configuração do modelo;
- treinamento;
- métricas;
- Column impact / feature importance;
- forecast;
- export;
- conclusões.

### AWS Free Tier

O SageMaker possui **Free Tier para contas elegíveis**. Atualmente, o SageMaker Canvas inclui até **160 horas/mês de sessão durante os primeiros 2 meses** do Free Tier.

> O Free Tier de sessão **não significa que todo treinamento ou previsão seja necessariamente gratuito**. Construção de modelos e predictions podem consumir recursos faturáveis; por isso a recomendação é verificar a elegibilidade da conta e encerrar a sessão após o laboratório.

Detalhes operacionais ficam fora do fluxo principal deste README e estão em `docs/10-custos-aws.md` e `docs/12-cleanup-aws.md`.

---

# 🐍 Trilha avançada — implementação própria em Python

A segunda versão implementa o mesmo problema de forecasting fora do Canvas.

## Stack

```text
Python 3.12
│
├── validação de dados
├── benchmarks de forecasting
├── rolling-origin backtesting
├── AutoGluon TimeSeries 1.6.1
├── probabilistic forecasting
├── métricas + calibration
├── Streamlit
└── GitHub Actions
```

### Por que criar essa segunda versão?

O Canvas mostra **como resolver o problema usando AutoML no-code**.

A versão Python mostra:

- como a validação é construída;
- como o split temporal funciona;
- como comparar modelos;
- como avaliar incerteza;
- como preservar resultados;
- como testar e automatizar a solução.

Isso transforma o laboratório em um case de portfólio com maior profundidade técnica.

---

# 📊 Protocolo experimental

## Rolling-origin / expanding-window

Foram utilizados 3 testes temporais externos não sobrepostos:

| Fold | Treino por SKU | Teste por SKU |
|---:|---:|---:|
| 1 | 19 dias | 7 dias |
| 2 | 26 dias | 7 dias |
| 3 | 33 dias | 7 dias |

O período externo não é usado para selecionar o modelo.

---

# 🥇 Baselines

| Modelo | WAPE médio | RMSE médio | MACRO_MASE | WQL médio |
|---|---:|---:|---:|---:|
| **Naive** | **0.739365** | **45.785757** | **2.588005** | **0.647723** |
| Drift | 0.809554 | 52.004579 | 2.853404 | 0.690580 |
| SeasonalNaive7 | 0.874120 | 49.939643 | 3.010651 | 0.818905 |

O Naive foi o baseline mais forte nas três janelas.

---

# 🤖 AutoGluon TimeSeries

Configuração executada:

```text
AutoGluon TimeSeries = 1.6.1
prediction_length = 7
freq = D
eval_metric = WQL
quantile_levels = [0.1, 0.5, 0.9]
known_covariates = [PRECO, FLAG_PROMOCAO]
random_seed = 123
presets = medium_quality
```

## Resultado dos três folds

| Fold | Modelo selecionado | Vencedor externo | Rank do WeightedEnsemble | WAPE | WQL |
|---:|---|---|---:|---:|---:|
| 1 | WeightedEnsemble | **Chronos2** | 3º | 0.700500 | 0.424289 |
| 2 | WeightedEnsemble | **WeightedEnsemble** | 1º | 0.441683 | 0.262329 |
| 3 | WeightedEnsemble | **WeightedEnsemble** | 1º | 0.358348 | 0.223493 |

### Leitura correta

- seleção interna do ensemble: **3/3 folds**;
- vitória externa: **2/3 folds**;
- estabilidade de seleção: **stable**;
- estabilidade externa: **unstable**.

O projeto não força a narrativa de que um único modelo é sempre superior.

---

# 📈 Ganho sobre o melhor baseline

Comparação média AutoGluon × Naive:

| Métrica | Naive | AutoGluon | Melhoria relativa |
|---|---:|---:|---:|
| WAPE | 0.739365 | **0.500177** | **32,35%** |
| RMSE | 45.785757 | **31.917570** | **30,29%** |
| WQL | 0.647723 | **0.303370** | **53,16%** |

Esses resultados pertencem ao dataset educacional deste projeto e não representam garantia de desempenho em produção.

---

# 🎯 Forecast probabilístico

Além de previsão pontual, o projeto avalia P10/P50/P90.

| Indicador | Resultado |
|---|---:|
| `y <= P10` | 20,95% |
| `y <= P50` | 51,05% |
| `y <= P90` | 88,19% |
| Coverage P10–P90 | **67,24%** |
| Coverage nominal | ~80% |
| Quantile crossing | **0** |

Conclusão: os intervalos representam incerteza, mas apresentam **subcoverage** neste histórico curto.

---

# 🖥️ Inventory Forecasting Studio

O projeto inclui um dashboard Streamlit para explorar:

- dataset e EDA;
- benchmarks;
- leaderboard AutoGluon;
- estabilidade dos modelos;
- calibration;
- forecast por SKU;
- P10/P50/P90;
- resultados validados.

Executar:

```bash
python -m venv .venv
pip install -r requirements-app.txt
streamlit run app.py
```

---

# 🧪 Engenharia e qualidade

## 25 testes automatizados

Cobrem:

- dataset/cardinalidade;
- duplicatas SKU+data;
- splits temporais;
- rolling-origin;
- métricas;
- probabilistic forecasting;
- AutoGluon contracts;
- UI;
- secret scanning;
- DIO submission readiness.

## CI

Workflows incluem:

- Dataset validation;
- Python forecasting;
- AutoGluon experiment;
- Streamlit smoke test;
- Security scan;
- DIO readiness.

---

# 🔐 Segurança

A trilha principal possui:

- secret scanning;
- `pip-audit`;
- GitHub Actions oficiais pinadas por commit SHA;
- `contents: read` nos workflows;
- separação entre dependências obrigatórias e stack ML opcional.

A extensão AutoGluon possui hoje um risco transitivo conhecido em `lightning 2.6.5` (`CVE-2026-58659 / PYSEC-2026-3624`). A trilha Canvas/DIO não depende dessa biblioteca.

Veja `SECURITY.md` para detalhes.

---

# 📦 Reprodutibilidade

Resultados pequenos e auditáveis estão preservados em:

```text
results/validated/
```

Incluindo:

- métricas multifold;
- summary agregado;
- estabilidade dos modelos;
- calibração por horizonte;
- análise por SKU;
- manifesto com hash do dataset;
- proveniência dos artifacts.

---

# 🔎 DIO Submission Readiness

Existe um checker automático:

```bash
python scripts/check_dio_submission.py
```

Hoje ele deve retornar:

```text
DIO SUBMISSION READY: NO
```

porque a evidência real do Canvas ainda não foi gerada.

Após completar o fluxo AWS:

```bash
python scripts/check_dio_submission.py --strict
```

O projeto só será marcado como pronto quando todas as evidências obrigatórias existirem.

---

# 📚 Evidências e documentação

| Documento | Finalidade |
|---|---|
| `docs/04-configuracao-sagemaker-canvas.md` | execução Canvas passo a passo |
| `docs/07-resultados-python.md` | resultados reais Python |
| `docs/13-checklist-submissao-dio.md` | checklist oficial da entrega |
| `docs/14-matriz-evidencias-dio.md` | requisito → evidência |
| `docs/15-resultados-canvas.md` | template para resultados reais AWS |
| `assets/screenshots/README.md` | protocolo de screenshots |
| `results/validated/` | evidências reproduzíveis da trilha Python |

---

# ⚠️ Limitações

- 40 observações por SKU;
- dataset educacional;
- forecast de estoque não equivale a forecast de demanda;
- reposições podem alterar a dinâmica observada;
- covariáveis futuras só são válidas quando realmente conhecidas;
- a solução Python é um demonstrador avançado, não um sistema corporativo completo de reposição.

---

# 🧭 Próxima evolução

Após fechar a trilha DIO, uma versão de produto real deveria evoluir de previsão de estoque para decisão operacional:

```text
DEMANDA / VENDAS
      ↓
FORECAST
      ↓
LEAD TIME
      ↓
SAFETY STOCK
      ↓
REORDER POINT
      ↓
QUANTIDADE RECOMENDADA
```

---

# ✅ Status final

| Trilha | Estado |
|---|---|
| Projeto original DIO | **Preservado e expandido** |
| Versão Python | **Executada e reproduzível** |
| CI / testes / segurança | **Implementados** |
| Documentação | **Estruturada** |
| SageMaker Canvas real | **Pendente** |
| Submissão DIO | **READY AFTER CANVAS** |

> **O projeto foi intencionalmente expandido além do laboratório original: a trilha Canvas mantém a aderência à DIO, enquanto a versão Python demonstra o mesmo problema com maior transparência metodológica, automação e reprodutibilidade.**
