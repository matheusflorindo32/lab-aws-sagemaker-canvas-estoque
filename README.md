# 📊 Previsão de Estoque Inteligente — AWS SageMaker Canvas

> Desafio de projeto da DIO com uma extensão open source adicional em Python/AutoGluon.

[![DIO](https://img.shields.io/badge/DIO-Project%20Lab-6C63FF)](https://www.dio.me/)
[![Dataset validation](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/dataset-validation.yml/badge.svg?branch=feat/professional-ml-portfolio)](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/dataset-validation.yml)
[![Security](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/security.yml/badge.svg?branch=feat/professional-ml-portfolio)](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/security.yml)

## 🎯 Objetivo

Este repositório parte do desafio oficial **“Previsão de Estoque Inteligente na AWS com SageMaker Canvas”** da Digital Innovation One.

O objetivo da trilha DIO é:

1. selecionar um dataset;
2. importar o dataset no Amazon SageMaker Canvas;
3. configurar as variáveis de entrada/saída;
4. treinar um modelo de forecasting;
5. analisar métricas e principais características;
6. gerar previsões de estoque;
7. exportar os resultados;
8. documentar conclusões e insights.

Além da trilha original, o repositório contém uma extensão opcional e já executada em Python para aprofundar forecasting, validação temporal e reprodutibilidade.

---

# ✅ Status do desafio DIO

| Etapa | Status |
|---|---|
| Fork do projeto | ✅ concluído |
| README reescrito | ✅ concluído |
| Dataset selecionado e validado | ✅ concluído |
| Upload/import no SageMaker Canvas | ⏳ pendente execução AWS |
| Configuração do modelo Canvas | ⏳ pendente execução AWS |
| Treinamento Canvas | ⏳ pendente execução AWS |
| Métricas/feature importance Canvas | ⏳ pendente execução AWS |
| Forecast Canvas | ⏳ pendente execução AWS |
| Export Canvas | ⏳ pendente execução AWS |
| Conclusões da execução Canvas | ⏳ pendente execução AWS |
| Envio da URL na DIO | ⏳ etapa final |

> **Nenhum resultado Python é apresentado como se fosse resultado do SageMaker Canvas.**

Checklist literal e evidências esperadas: [`docs/13-checklist-submissao-dio.md`](docs/13-checklist-submissao-dio.md).

---

# 📁 Dataset escolhido

Arquivo:

```text
datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv
```

Validação automatizada:

| Propriedade | Resultado |
|---|---:|
| Registros | 1.000 |
| SKUs | 25 |
| Observações por SKU | 40 |
| Frequência | diária |
| Período | 2023-12-31 a 2024-02-08 |
| Missing | 0 |
| Duplicatas exatas | 0 |
| Duplicatas `SKU + data` | 0 |
| Pontos diários ausentes | 0 |
| Linhas inválidas | 0 |

Campos:

| Campo | Papel |
|---|---|
| `ID_PRODUTO` | identificador do item/SKU |
| `DATA_EVENTO` | timestamp |
| `PRECO` | covariável |
| `FLAG_PROMOCAO` | covariável |
| `QUANTIDADE_ESTOQUE` | target |

---

# ☁️ Configuração planejada no SageMaker Canvas

| Parâmetro | Configuração |
|---|---|
| Tipo | Time Series Forecasting |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Frequência | Daily |
| Horizonte | 7 dias |
| Covariáveis | `PRECO`, `FLAG_PROMOCAO` |

Guia passo a passo: [`docs/04-configuracao-sagemaker-canvas.md`](docs/04-configuracao-sagemaker-canvas.md).

> A configuração acima é o plano preparado. Na execução real, deve-se registrar exatamente as opções que a interface atual do Canvas disponibilizar.

---

# 📸 Evidências que serão adicionadas após a execução AWS

Somente screenshots reais e sanitizados serão versionados em `assets/screenshots/`:

1. `01-canvas-home.png`
2. `02-import-dataset.png`
3. `03-dataset-preview.png`
4. `04-model-configuration.png`
5. `05-training.png`
6. `06-model-analysis.png`
7. `07-feature-importance.png`
8. `08-forecast.png`
9. `09-export.png`

Não serão publicados Account ID, e-mail, IAM username, ARNs sensíveis, tokens, access keys ou dados pessoais de billing.

---

# 🐍 Extensão opcional — Inventory Forecasting Studio

A extensão Python não substitui a execução exigida pela DIO. Ela demonstra uma abordagem reproduzível do mesmo problema com:

- benchmarks `Naive`, `Drift` e `SeasonalNaive7`;
- AutoGluon TimeSeries 1.6.1;
- 3 folds rolling-origin/expanding-window;
- MAE, RMSE, WAPE, MAPE, WQL e `MACRO_MASE`;
- P10/P50/P90;
- calibração probabilística;
- diagnóstico por SKU;
- Streamlit;
- testes e GitHub Actions.

## Resultado agregado dos três folds

| Métrica | AutoGluon | Melhor baseline (`Naive`) |
|---|---:|---:|
| WAPE médio | **0.500177** | 0.739365 |
| RMSE médio | **31.917570** | 45.785757 |
| WQL médio | **0.303370** | 0.647723 |

O `WeightedEnsemble` foi selecionado internamente em 3/3 folds, mas venceu externamente somente 2/3. No primeiro fold, `Chronos2` apresentou WQL melhor. Portanto, o projeto não afirma superioridade universal do ensemble.

Coverage observado do intervalo P10–P90: **67,24%**, abaixo dos ~80% nominais. Os quantis existem, mas não estão perfeitamente calibrados.

Resultados auditáveis: [`results/validated/`](results/validated/).

Detalhes: [`docs/07-resultados-python.md`](docs/07-resultados-python.md).

---

# 🖥️ Streamlit

```bash
python -m venv .venv
pip install -r requirements-app.txt
streamlit run app.py
```

O Studio apresenta dataset, EDA, benchmarks, forecast, estabilidade temporal e calibração.

---

# 🔐 Segurança

O caminho obrigatório da submissão DIO possui:

- secret-pattern scanning;
- workflows com `contents: read`;
- GitHub Actions oficiais pinadas por SHA;
- `pip-audit` obrigatório sobre as dependências da aplicação **sem vulnerabilidades ignoradas**.

A extensão AutoGluon possui uma dependência transitiva `lightning 2.6.5` afetada por `CVE-2026-58659 / PYSEC-2026-3624`. Em 30/08/2026 ainda não existe release PyPI corrigida. Por isso:

- AutoGluon é tratado como **extensão opcional de portfólio**, não requisito da submissão DIO;
- o finding continua visível em um audit separado;
- checkpoints externos/não confiáveis não são aceitos pelo projeto;
- nenhuma exceção de CVE é usada no gate obrigatório da submissão DIO.

Veja [`SECURITY.md`](SECURITY.md).

---

# 🧪 Qualidade e CI

A trilha Python possui **23 testes** e validações para:

- integridade/cardinalidade do dataset;
- unicidade `SKU + data`;
- splits temporais;
- rolling-origin sem sobreposição externa;
- métricas de forecasting;
- métricas probabilísticas;
- benchmarks;
- contratos AutoGluon;
- UI;
- secret scanner.

---

# ⚠️ Limitações

- apenas 40 observações por SKU;
- dataset educacional;
- forecast de estoque não equivale a forecast de demanda;
- reposições/reset são intervenções operacionais;
- `PRECO` e `FLAG_PROMOCAO` só são covariáveis futuras válidas se seus valores forem conhecidos no horizonte;
- a extensão Python é demonstrador/portfólio, não sistema empresarial de reposição automática.

---

# 💰 Custos AWS

SageMaker Canvas pode gerar cobrança. Nenhum recurso potencialmente faturável deve ser iniciado sem revisão de custos e autorização explícita.

Plano FinOps e cleanup: [`docs/10-custos-aws.md`](docs/10-custos-aws.md) e [`docs/12-cleanup-aws.md`](docs/12-cleanup-aws.md).

---

# 📋 Antes de enviar para a DIO

A submissão só deve ser feita depois de:

- [ ] executar o SageMaker Canvas;
- [ ] adicionar screenshots reais;
- [ ] registrar métricas reais do Canvas;
- [ ] registrar feature importance real;
- [ ] gerar/exportar forecast real;
- [ ] escrever conclusões da execução;
- [ ] confirmar que nenhum dado sensível aparece nas imagens;
- [ ] fazer logout/cleanup da AWS;
- [ ] verificar CI final;
- [ ] atualizar este README de `pendente` para `executado` nas etapas realmente concluídas.

**Estado atual: ainda não enviar à DIO porque a etapa real do SageMaker Canvas continua pendente.**
