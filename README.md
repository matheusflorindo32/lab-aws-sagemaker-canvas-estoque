# ✨ Previsão de Estoque Inteligente — DIO + AWS SageMaker Canvas + Python

> **Desafio oficial DIO transformado em um case completo de forecasting com duas trilhas complementares:** a experiência no-code do **Amazon SageMaker Canvas** e uma implementação própria, interativa, reproduzível e auditável em **Python + AutoGluon + Streamlit**.

[![DIO](https://img.shields.io/badge/DIO-Project%20Challenge-6C63FF)](https://www.dio.me/)
[![AWS](https://img.shields.io/badge/AWS-SageMaker%20Canvas-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/sagemaker/ai/canvas/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![AutoGluon](https://img.shields.io/badge/AutoGluon-TimeSeries-4B8BBE)](https://auto.gluon.ai/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20Studio-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

---

## 💎 Executive Project Board

| Dimensão | Status | Entrega |
|---|---|---|
| 🎯 Desafio DIO | **Preparado** | fluxo oficial reconstruído e documentado |
| ☁️ SageMaker Canvas | **Execução real pendente** | import → build → métricas → forecast → export |
| 🐍 Versão própria em Python | **Executada** | forecasting programático e reproduzível |
| 📤 Teste por terceiros | **Implementado** | dataset demo ou upload de CSV próprio |
| 🧪 Validação histórica | **Implementada** | holdout temporal com comparação previsão × valor real |
| 🔮 Previsão futura | **Implementada** | usa todo o histórico e gera datas posteriores ao dataset |
| 📊 Validação científica | **Executada** | 3 folds rolling-origin / expanding-window |
| 🤖 AutoML | **Executado** | AutoGluon TimeSeries 1.6.1 |
| 🎯 Forecast probabilístico | **Executado** | P10 / P50 / P90 + calibration |
| 🖥️ Dashboard | **Executado** | Inventory Forecasting Studio em Streamlit |
| 🧪 Qualidade | **27 testes** | dados, forecasting, segurança e readiness |
| 🔐 Segurança | **Hardened** | secret scan, pip-audit e Actions pinadas por SHA |
| 🚀 Submissão DIO | **READY AFTER CANVAS** | falta a evidência real da execução AWS |

---

# 🎯 Sobre o desafio DIO

Este projeto nasceu do desafio **“Previsão de Estoque Inteligente na AWS com SageMaker Canvas”** da Digital Innovation One.

O fluxo da atividade é:

1. escolher um dataset;
2. importar os dados no Amazon SageMaker Canvas;
3. configurar o problema de previsão;
4. treinar o modelo;
5. analisar métricas e características relevantes;
6. gerar previsões;
7. exportar os resultados;
8. registrar conclusões;
9. enviar o link do repositório na DIO.

A trilha Canvas foi preservada. A versão Python é uma **evolução adicional do projeto**, não uma substituição silenciosa da atividade original.

---

# 🚀 Como o projeto original foi evoluído

O laboratório deixou de ser apenas uma execução visual e ganhou uma segunda implementação completa e aberta.

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
               model build             backtesting temporal
                    │                       │
              metrics / impact         baselines + AutoGluon
                    │                       │
                  forecast             P10 / P50 / P90
                    │                       │
                   export              Streamlit Studio
                    │                       │
                    │              upload CSV + forecast futuro
                    └───────────┬───────────┘
                                ▼
                       ANÁLISE COMPARATIVA
```

### Modificações e extensões implementadas

- validação automatizada do dataset;
- checagem de cardinalidade e duplicatas `SKU + data`;
- análise exploratória;
- baselines `Naive`, `Drift` e `SeasonalNaive7`;
- backtest/holdout temporal;
- 3 folds rolling-origin / expanding-window;
- AutoGluon TimeSeries;
- MAE, RMSE, WAPE, MAPE, WQL e `MACRO_MASE`;
- P10/P50/P90, coverage e calibração;
- diagnóstico por SKU e horizonte;
- **upload de CSV pelo usuário**;
- **modo Validação histórica**;
- **modo Previsão futura**;
- export de resultados em CSV;
- dashboard Streamlit;
- testes automatizados;
- GitHub Actions;
- dependency audit e secret scanning;
- artifacts e manifestos reproduzíveis;
- readiness checker específico para submissão DIO.

---

# 🧠 Duas perguntas diferentes: testar e prever

Uma das melhorias mais importantes desta versão é deixar explícita a diferença entre **backtesting** e **forecast futuro**.

## 🧪 Modo 1 — Validação histórica

As datas de teste pertencem ao próprio histórico.

Exemplo conceitual:

```text
Histórico disponível: 01/01 → 08/02

Treino:              01/01 → 01/02
Dados escondidos:    02/02 → 08/02
                         ↓
                    modelo prevê
                         ↓
             previsão × valor real
                         ↓
                  MAE / RMSE / WAPE
```

Esse modo responde:

> **“Se eu estivesse naquele ponto do passado, quanto o modelo teria acertado?”**

Como os valores reais já existem, é possível medir o erro.

## 🔮 Modo 2 — Previsão futura

O segundo modo usa **todo o histórico** disponível e começa no dia seguinte à última observação de cada SKU.

No dataset de demonstração, cuja última data é `2024-02-08`, um horizonte de 7 dias produz datas futuras a partir de:

```text
2024-02-09 → 2024-02-15
```

Essas datas não possuem `actual`, porque naquele momento estamos realmente extrapolando o histórico.

Esse modo responde:

> **“Dado tudo o que conheço até hoje, qual é a projeção para os próximos dias?”**

---

# 🖥️ Inventory Forecasting Studio — teste você mesmo

O Studio foi preparado para que outra pessoa consiga experimentar o projeto sem alterar código.

### Opção A — dataset de demonstração

Selecione:

`Dataset de demonstração`

### Opção B — seu próprio CSV

Selecione:

`Enviar meu CSV`

O arquivo deve conter:

```text
ID_PRODUTO,DATA_EVENTO,PRECO,FLAG_PROMOCAO,QUANTIDADE_ESTOQUE
```

Formato esperado de data:

```text
YYYY-MM-DD
```

Depois escolha uma das experiências:

### 🧪 Validação histórica

- define o horizonte;
- esconde as últimas observações;
- calcula previsões;
- compara com os valores reais;
- apresenta métricas;
- permite download do backtest.

### 🔮 Previsão futura

- usa todo o histórico;
- escolhe `Naive`, `SeasonalNaive7` ou `Drift`;
- cria datas futuras automaticamente;
- gera `point`, `P10`, `P50` e `P90`;
- permite visualizar por SKU;
- permite baixar `future_inventory_forecast.csv`.

> O modo futuro leve usa os baselines do projeto para manter o aplicativo público rápido e barato. O AutoGluon permanece como experimento avançado reproduzível por script e com resultados validados versionados.

---

# ▶️ Executar localmente

```bash
# clone o repositório
git clone https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque.git
cd lab-aws-sagemaker-canvas-estoque

# use a branch do projeto enquanto o PR estiver aberto
git checkout feat/professional-ml-portfolio

# ambiente
python -m venv .venv
pip install -r requirements-app.txt

# aplicação
streamlit run app.py
```

O navegador abrirá o **Inventory Forecasting Studio**.

---

# 🌐 Deploy público

A aplicação está preparada para **Streamlit Community Cloud**, que é a opção natural para esta versão porque o frontend e o motor leve estão na mesma aplicação Python.

Configuração de deploy:

```text
Repository: matheusflorindo32/lab-aws-sagemaker-canvas-estoque
Branch: feat/professional-ml-portfolio
Main file: app.py
Requirements: requirements-app.txt
```

> O link público será adicionado aqui após o primeiro deploy. Não é necessário migrar para Vercel para demonstrar esta versão. Uma futura V2 SaaS pode separar frontend web e API Python.

---

# 📁 Dataset de demonstração

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

Configuração preparada:

| Parâmetro | Valor planejado |
|---|---|
| Problem type | Time Series Forecasting |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Forecast length | **7 dias** |
| Frequência | diária |
| Colunas adicionais | `PRECO`, `FLAG_PROMOCAO` quando suportadas pelo fluxo real |

**Status: execução real do Canvas ainda pendente.**

Nenhum resultado Python é apresentado como resultado AWS.

Após a execução serão adicionadas evidências reais de:

- import;
- configuração;
- treinamento;
- métricas;
- Column impact / feature importance;
- forecast;
- export;
- conclusões.

### AWS Free Tier

O SageMaker Canvas possui Free Tier para contas elegíveis. A elegibilidade e eventuais cobranças de build/prediction devem ser verificadas na própria conta antes da execução.

Detalhes operacionais: `docs/10-custos-aws.md` e `docs/12-cleanup-aws.md`.

---

# 🐍 Trilha avançada — Python + AutoGluon

## Stack

```text
Python 3.12
│
├── validação de dados
├── upload de CSV
├── historical backtesting
├── future forecasting
├── rolling-origin
├── AutoGluon TimeSeries 1.6.1
├── probabilistic forecasting
├── métricas + calibration
├── Streamlit
└── GitHub Actions
```

O Canvas mostra **como resolver o problema usando AutoML no-code**.

A versão Python expõe a mecânica da solução, permite testes por terceiros e adiciona reprodutibilidade.

---

# 📊 Protocolo científico

Foram utilizados 3 testes temporais externos não sobrepostos:

| Fold | Treino por SKU | Teste por SKU |
|---:|---:|---:|
| 1 | 19 dias | 7 dias |
| 2 | 26 dias | 7 dias |
| 3 | 33 dias | 7 dias |

O período externo não é usado para selecionar o modelo.

## Baselines

| Modelo | WAPE médio | RMSE médio | MACRO_MASE | WQL médio |
|---|---:|---:|---:|---:|
| **Naive** | **0.739365** | **45.785757** | **2.588005** | **0.647723** |
| Drift | 0.809554 | 52.004579 | 2.853404 | 0.690580 |
| SeasonalNaive7 | 0.874120 | 49.939643 | 3.010651 | 0.818905 |

---

# 🤖 AutoGluon TimeSeries

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

| Fold | Modelo selecionado | Vencedor externo | Rank WeightedEnsemble | WAPE | WQL |
|---:|---|---|---:|---:|---:|
| 1 | WeightedEnsemble | **Chronos2** | 3º | 0.700500 | 0.424289 |
| 2 | WeightedEnsemble | **WeightedEnsemble** | 1º | 0.441683 | 0.262329 |
| 3 | WeightedEnsemble | **WeightedEnsemble** | 1º | 0.358348 | 0.223493 |

- seleção interna: **3/3 folds**;
- vitória externa: **2/3 folds**;
- estabilidade externa: **unstable**.

O projeto preserva o resultado negativo do fold 1 em vez de vender o melhor holdout como regra geral.

---

# 📈 AutoGluon × melhor baseline

| Métrica | Naive | AutoGluon | Melhoria relativa |
|---|---:|---:|---:|
| WAPE | 0.739365 | **0.500177** | **32,35%** |
| RMSE | 45.785757 | **31.917570** | **30,29%** |
| WQL | 0.647723 | **0.303370** | **53,16%** |

Resultados pertencem ao dataset educacional e não são garantia de desempenho em produção.

---

# 🎯 Forecast probabilístico

| Indicador | Resultado |
|---|---:|
| `y <= P10` | 20,95% |
| `y <= P50` | 51,05% |
| `y <= P90` | 88,19% |
| Coverage P10–P90 | **67,24%** |
| Coverage nominal | ~80% |
| Quantile crossing | **0** |

Os intervalos apresentam subcoverage neste histórico curto.

---

# 🧪 Engenharia, testes e CI

A suíte agora possui **27 testes automatizados**, incluindo contratos para:

- parsing de CSV enviado pelo usuário;
- geração de datas futuras;
- ausência de `actual` em forecasts futuros;
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

A extensão AutoGluon possui risco transitivo conhecido em `lightning 2.6.5` (`CVE-2026-58659 / PYSEC-2026-3624`). A trilha Canvas/DIO e o app Streamlit leve não dependem dessa biblioteca.

Veja `SECURITY.md`.

---

# 📦 Reprodutibilidade

Resultados auditáveis estão em:

```text
results/validated/
```

Incluindo métricas multifold, estabilidade, calibração, análise por SKU e manifesto com hash do dataset.

---

# 🔎 DIO Submission Readiness

```bash
python scripts/check_dio_submission.py
```

Hoje:

```text
DIO SUBMISSION READY: NO
```

Após executar o Canvas e adicionar evidências reais:

```bash
python scripts/check_dio_submission.py --strict
```

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

- 40 observações por SKU no dataset demo;
- dataset educacional;
- forecast de estoque não equivale a forecast de demanda;
- reposições podem alterar a dinâmica observada;
- covariáveis futuras só são válidas quando realmente conhecidas;
- P10/P50/P90 dos baselines futuros são cenários empíricos, não intervalos perfeitamente calibrados;
- a solução é um demonstrador técnico avançado, não um sistema corporativo completo de reposição.

---

# 🧭 Próxima evolução

Após fechar a trilha DIO, uma versão de produto real deve evoluir de previsão para decisão operacional:

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
| Upload de CSV | **Implementado** |
| Validação histórica | **Implementada** |
| Previsão futura | **Implementada** |
| Versão Python | **Executada e reproduzível** |
| CI / testes / segurança | **Implementados** |
| Deploy público | **Preparado para Streamlit Community Cloud** |
| SageMaker Canvas real | **Pendente** |
| Submissão DIO | **READY AFTER CANVAS** |

> **O projeto foi intencionalmente expandido além do laboratório original: a trilha Canvas mantém a aderência à DIO, enquanto a implementação Python permite que qualquer pessoa valide o histórico, envie seu próprio CSV e gere previsões futuras diretamente pelo Studio.**
