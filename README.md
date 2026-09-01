# 💎 Previsão de Estoque Inteligente — DIO + AWS SageMaker Canvas + Python

> **Desafio oficial da DIO evoluído para um case completo de forecasting com duas trilhas complementares:** a implementação no-code prevista pelo desafio em **Amazon SageMaker Canvas** e uma versão própria, aberta, interativa e reproduzível em **Python + AutoGluon + Streamlit**.

[![DIO](https://img.shields.io/badge/DIO-Project%20Challenge-6C63FF)](https://www.dio.me/)
[![AWS](https://img.shields.io/badge/AWS-SageMaker%20Canvas-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/sagemaker/ai/canvas/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit&logoColor=white)](https://inventory-forecasting-studio.streamlit.app)
[![AutoGluon](https://img.shields.io/badge/AutoGluon-TimeSeries-4B8BBE)](https://auto.gluon.ai/)

## 🚀 Live Demo

**Aplicação pública:**  
https://inventory-forecasting-studio.streamlit.app

A versão publicada permite que qualquer pessoa teste o projeto diretamente no navegador usando o dataset de demonstração ou enviando seu próprio arquivo CSV.

---

## 💎 Executive Project Board

| Dimensão | Status | Entrega |
|---|---|---|
| 🎯 Desafio DIO | **Preservado e expandido** | fluxo oficial documentado |
| ☁️ SageMaker Canvas | **Trilha oficial preparada** | import → build → métricas → forecast → export |
| 🐍 Versão própria em Python | **Executada** | forecasting programático e reproduzível |
| 🌐 Aplicação pública | **ONLINE** | Streamlit Community Cloud |
| 📤 Teste por terceiros | **Implementado** | dataset demo ou upload de CSV |
| 🧪 Validação histórica | **Implementada** | previsão × valor real em holdout temporal |
| 🔮 Previsão futura | **Implementada** | projeção após a última data do histórico |
| 📊 Validação temporal | **Executada** | 3 folds rolling-origin / expanding-window |
| 🤖 AutoML | **Executado** | AutoGluon TimeSeries 1.6.1 |
| 🎯 Incerteza | **Avaliada** | P10 / P50 / P90 + coverage |
| 🧪 Qualidade | **27 testes** | dados, forecasting, UI, segurança e readiness |
| 🔐 Segurança | **Hardened** | secret scan, dependency audit e CI |
| 🚀 Submissão DIO | **READY AFTER CANVAS** | falta apenas a execução/evidência real da trilha AWS |

---

# 🎯 Sobre o projeto

Este projeto nasceu do desafio **“Previsão de Estoque Inteligente na AWS com SageMaker Canvas”**, da Digital Innovation One.

A proposta original é utilizar o **Amazon SageMaker Canvas** para trabalhar com previsão de estoque por séries temporais em um fluxo visual/no-code.

Em vez de apenas reproduzir o laboratório, eu mantive essa trilha oficial e desenvolvi uma **segunda implementação completa em Python**, permitindo estudar, testar e executar o mesmo tipo de problema de forecasting de forma aberta e reproduzível.

O resultado é um projeto com duas possibilidades:

### ☁️ Opção 1 — Amazon SageMaker Canvas

Seguir a proposta original da DIO utilizando o ambiente AutoML/no-code da AWS.

### 🐍 Opção 2 — Python + Streamlit

Executar a solução de forecasting sem depender obrigatoriamente do SageMaker Canvas para experimentar o projeto.

A versão Python permite:

- analisar os dados;
- validar modelos historicamente;
- gerar previsões futuras;
- enviar um CSV próprio;
- visualizar resultados por SKU;
- exportar previsões;
- reproduzir os experimentos localmente;
- acessar uma demonstração pública no navegador.

> **Importante:** a versão Python é uma extensão funcional/open source do projeto e não é apresentada como se fosse uma execução do SageMaker Canvas. A trilha AWS permanece separada e documentada para manter aderência ao desafio original da DIO.

---

# 🧩 O que foi modificado em relação ao projeto original

O laboratório foi ampliado com uma camada adicional de engenharia de software, ciência de dados e experiência de uso.

Foram adicionados:

- validação automatizada do dataset;
- checagem de cardinalidade e duplicatas `SKU + data`;
- análise exploratória;
- baselines `Naive`, `Drift` e `SeasonalNaive7`;
- backtesting temporal;
- 3 folds rolling-origin / expanding-window;
- AutoGluon TimeSeries;
- métricas MAE, RMSE, WAPE, MAPE, WQL e `MACRO_MASE`;
- previsões probabilísticas P10/P50/P90;
- análise de coverage e calibração;
- diagnóstico por SKU e horizonte;
- upload de CSV pelo usuário;
- modo **Validação histórica**;
- modo **Previsão futura**;
- exportação dos resultados em CSV;
- dashboard Streamlit;
- deploy público;
- testes automatizados;
- GitHub Actions;
- secret scanning;
- dependency audit;
- artifacts e manifestos reproduzíveis;
- readiness checker específico para a entrega DIO.

---

# 🏗️ Arquitetura

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
                                            │
                                   upload CSV + forecast futuro
                                            │
                                            ▼
                                    🌐 LIVE APPLICATION
```

---

# 🌐 Teste agora no navegador

Abra:

**https://inventory-forecasting-studio.streamlit.app**

No painel lateral você pode escolher:

### Dataset de demonstração

Usa o dataset versionado no próprio repositório.

### Enviar meu CSV

Permite testar outro conjunto de dados sem alterar o código.

Schema esperado:

```text
ID_PRODUTO,DATA_EVENTO,PRECO,FLAG_PROMOCAO,QUANTIDADE_ESTOQUE
```

Formato da data:

```text
YYYY-MM-DD
```

---

# 🧪 Validação histórica × 🔮 Previsão futura

As duas funções têm objetivos diferentes.

## 🧪 Validação histórica

O sistema esconde as últimas observações do histórico, treina com o período anterior e compara a previsão com valores que já conhecemos.

```text
HISTÓRICO
01/01 ───────────────────────────── 08/02

TREINO
01/01 ───────────────── 01/02

HOLDOUT / TESTE
                       02/02 ────── 08/02
                              │
                              ▼
                     previsão × valor real
                              │
                              ▼
                     MAE / RMSE / WAPE
```

Esse modo responde:

> **“Se o modelo estivesse naquele ponto do passado, quanto ele teria acertado?”**

Por isso as datas vistas no backtest pertencem ao dataset histórico: elas são usadas para medir erro.

## 🔮 Previsão futura

O sistema utiliza todo o histórico disponível e gera novas datas posteriores à última observação.

No dataset demo:

```text
Última observação real: 2024-02-08
Horizonte: 7 dias

Forecast futuro:
2024-02-09 → 2024-02-15
```

Não existe coluna `actual` nessas datas futuras porque o valor real ainda não é conhecido.

Esse modo responde:

> **“Com tudo o que sei até agora, qual é a projeção para os próximos dias?”**

---

# 📁 Dataset de demonstração

Arquivo:

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
| `ID_PRODUTO` | Item ID / SKU |
| `DATA_EVENTO` | timestamp |
| `PRECO` | variável adicional |
| `FLAG_PROMOCAO` | variável adicional |
| `QUANTIDADE_ESTOQUE` | target |

---

# 🐍 Versão Python

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

## Baselines disponíveis no app público

- `Naive`
- `SeasonalNaive7`
- `Drift`

Esses modelos permitem que o aplicativo público permaneça leve e rápido.

O AutoGluon é mantido como experimento avançado, reproduzível por script, com resultados validados e versionados no repositório.

---

# 📊 Protocolo experimental

Foram utilizados 3 testes temporais externos não sobrepostos:

| Fold | Treino por SKU | Teste por SKU |
|---:|---:|---:|
| 1 | 19 dias | 7 dias |
| 2 | 26 dias | 7 dias |
| 3 | 33 dias | 7 dias |

Isso reduz o risco de avaliar o modelo apenas em uma única janela temporal.

## Baselines

| Modelo | WAPE médio | RMSE médio | MACRO_MASE | WQL médio |
|---|---:|---:|---:|---:|
| **Naive** | **0.739365** | **45.785757** | **2.588005** | **0.647723** |
| Drift | 0.809554 | 52.004579 | 2.853404 | 0.690580 |
| SeasonalNaive7 | 0.874120 | 49.939643 | 3.010651 | 0.818905 |

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

| Fold | Modelo selecionado | Vencedor externo | Rank WeightedEnsemble | WAPE | WQL |
|---:|---|---|---:|---:|---:|
| 1 | WeightedEnsemble | **Chronos2** | 3º | 0.700500 | 0.424289 |
| 2 | WeightedEnsemble | **WeightedEnsemble** | 1º | 0.441683 | 0.262329 |
| 3 | WeightedEnsemble | **WeightedEnsemble** | 1º | 0.358348 | 0.223493 |

- seleção interna do ensemble: **3/3 folds**;
- vitória externa: **2/3 folds**;
- estabilidade externa: **unstable**.

O projeto preserva o resultado menos favorável do primeiro fold em vez de apresentar apenas o melhor cenário.

---

# 📈 AutoGluon × melhor baseline

| Métrica | Naive | AutoGluon | Melhoria relativa |
|---|---:|---:|---:|
| WAPE | 0.739365 | **0.500177** | **32,35%** |
| RMSE | 45.785757 | **31.917570** | **30,29%** |
| WQL | 0.647723 | **0.303370** | **53,16%** |

Esses resultados pertencem ao dataset educacional e não representam garantia de desempenho em produção.

---

# 🎯 Forecast probabilístico

| Indicador | Resultado |
|---|---:|
| `y <= P10` | 20,95% |
| `y <= P50` | 51,05% |
| `y <= P90` | 88,19% |
| Coverage P10–P90 | **67,24%** |
| Coverage nominal | ~80% |
| Quantile crossings | **0** |

Os intervalos representam cenários de incerteza, mas o coverage observado mostra que a calibração ainda não é perfeita.

---

# ☁️ Trilha oficial — Amazon SageMaker Canvas

A configuração planejada para o desafio DIO é:

| Parâmetro | Valor |
|---|---|
| Problem type | Time Series Forecasting |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Forecast length | **7 dias** |
| Frequência | diária |
| Colunas adicionais | `PRECO`, `FLAG_PROMOCAO` quando suportadas pelo fluxo real |

A execução real do Canvas permanece separada da versão Python.

Quando realizada, a trilha AWS deverá registrar evidências de:

- import do dataset;
- configuração do modelo;
- treinamento;
- métricas;
- Column impact / feature importance;
- forecast;
- export;
- conclusões.

## AWS e opção de executar sem AWS

O SageMaker Canvas possui Free Tier para contas elegíveis, mas a elegibilidade e eventuais cobranças de build/prediction devem ser verificadas na própria conta.

Para quem quiser **apenas experimentar o problema de forecasting**, a aplicação Python publicada no Streamlit oferece uma alternativa gratuita/open source para testar o fluxo sem precisar criar recursos no SageMaker Canvas.

Isso não altera a distinção entre as duas trilhas:

```text
DIO / Canvas = implementação oficial do desafio
Python / Streamlit = extensão própria e alternativa de demonstração
```

Detalhes operacionais da AWS estão em:

- `docs/04-configuracao-sagemaker-canvas.md`
- `docs/10-custos-aws.md`
- `docs/12-cleanup-aws.md`

---

# ▶️ Executar localmente

```bash
git clone https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque.git
cd lab-aws-sagemaker-canvas-estoque
git checkout feat/professional-ml-portfolio

python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

---

# 🌐 Deploy

A aplicação está publicada no **Streamlit Community Cloud**.

**Live Demo:**  
https://inventory-forecasting-studio.streamlit.app

Configuração utilizada:

```text
Repository: matheusflorindo32/lab-aws-sagemaker-canvas-estoque
Branch: feat/professional-ml-portfolio
Main file: app.py
Dependencies: requirements.txt
```

---

# 🧪 Engenharia e qualidade

A suíte atual possui **27 testes automatizados** cobrindo, entre outros pontos:

- dataset/cardinalidade;
- duplicatas SKU+data;
- upload de CSV;
- splits temporais;
- rolling-origin;
- métricas;
- future forecasting;
- probabilistic forecasting;
- contratos AutoGluon;
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

Resultados auditáveis estão preservados em:

```text
results/validated/
```

Incluindo métricas multifold, estabilidade, calibração, análise por SKU e manifesto com hash do dataset.

---

# 🔎 DIO Submission Readiness

```bash
python scripts/check_dio_submission.py
```

Estado atual:

```text
DIO SUBMISSION READY: NO
```

O motivo é objetivo: ainda faltam as evidências da execução real do SageMaker Canvas.

Depois dessa etapa:

```bash
python scripts/check_dio_submission.py --strict
```

---

# 📚 Documentação

| Documento | Finalidade |
|---|---|
| `docs/04-configuracao-sagemaker-canvas.md` | execução Canvas passo a passo |
| `docs/07-resultados-python.md` | resultados Python |
| `docs/13-checklist-submissao-dio.md` | checklist da entrega |
| `docs/14-matriz-evidencias-dio.md` | requisito → evidência |
| `docs/15-resultados-canvas.md` | resultados reais AWS após execução |
| `assets/screenshots/README.md` | protocolo de screenshots |
| `results/validated/` | evidências reproduzíveis da trilha Python |

---

# ⚠️ Limitações

- dataset educacional com 40 observações por SKU;
- forecast de estoque não equivale a forecast de demanda;
- reposições podem alterar a dinâmica observada;
- covariáveis futuras só são válidas quando seus valores futuros são realmente conhecidos;
- P10/P50/P90 dos baselines públicos são cenários empíricos;
- a solução é um demonstrador técnico avançado, não um sistema corporativo completo de reposição automática.

---

# 🧭 Próxima evolução

Uma evolução de produto real deveria transformar previsão em decisão operacional:

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
| Aplicação pública | **ONLINE** |
| Upload de CSV | **Implementado** |
| Validação histórica | **Implementada** |
| Previsão futura | **Implementada** |
| Versão Python | **Executada e reproduzível** |
| CI / testes / segurança | **Implementados** |
| SageMaker Canvas real | **Pendente** |
| Submissão DIO | **READY AFTER CANVAS** |

> **O projeto foi intencionalmente expandido além do laboratório original: a trilha Canvas mantém a aderência à DIO, enquanto a implementação Python permite que qualquer pessoa teste o problema, envie seu próprio CSV, valide o histórico e gere previsões futuras diretamente pelo navegador.**

---

## 🔗 Links

**GitHub:**  
https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/tree/feat/professional-ml-portfolio

**Live Demo:**  
https://inventory-forecasting-studio.streamlit.app
