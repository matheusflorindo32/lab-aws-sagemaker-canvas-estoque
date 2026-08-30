# 📊 Previsão de Estoque Inteligente — AWS SageMaker Canvas

> Desafio de projeto da DIO com uma extensão open source adicional e claramente separada em Python/AutoGluon.

[![DIO](https://img.shields.io/badge/DIO-Project%20Lab-6C63FF)](https://www.dio.me/)
[![Dataset validation](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/dataset-validation.yml/badge.svg?branch=feat/professional-ml-portfolio)](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/dataset-validation.yml)
[![Security](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/security.yml/badge.svg?branch=feat/professional-ml-portfolio)](https://github.com/matheusflorindo32/lab-aws-sagemaker-canvas-estoque/actions/workflows/security.yml)

# 🎯 Projeto DIO — SageMaker Canvas

Este repositório parte do desafio oficial **“Previsão de Estoque Inteligente na AWS com SageMaker Canvas”** da Digital Innovation One.

A trilha obrigatória do desafio é:

1. selecionar um dataset;
2. fazer upload/import no Amazon SageMaker Canvas;
3. configurar variáveis de entrada e saída;
4. treinar um modelo de forecasting;
5. analisar métricas e características que influenciam as previsões;
6. gerar previsões de estoque;
7. exportar os resultados;
8. documentar conclusões e insights;
9. enviar a URL deste repositório na plataforma DIO.

A extensão Python/AutoGluon existente neste repositório é **opcional e adicional**. Ela não substitui nenhuma etapa do SageMaker Canvas.

---

# ✅ Status DIO

**DIO SUBMISSION READY: NO**

| Etapa | Status |
|---|---|
| Fork do projeto | ✅ PASS |
| README reescrito | ✅ PASS |
| Dataset selecionado e validado | ✅ PASS |
| Upload/import no SageMaker Canvas | ⏳ PENDING AWS |
| Configuração real do modelo Canvas | ⏳ PENDING AWS |
| Treinamento Canvas | ⏳ PENDING AWS |
| Métricas/Column impact Canvas | ⏳ PENDING AWS |
| Forecast Canvas | ⏳ PENDING AWS |
| Export Canvas | ⏳ PENDING AWS |
| Conclusões da execução Canvas | ⏳ PENDING AWS |
| Envio da URL na DIO | ⏳ etapa final |

> **Nenhum resultado Python é apresentado como resultado do SageMaker Canvas.**

Fontes de verdade para a entrega:

- checklist literal: [`docs/13-checklist-submissao-dio.md`](docs/13-checklist-submissao-dio.md)
- matriz de evidências: [`docs/14-matriz-evidencias-dio.md`](docs/14-matriz-evidencias-dio.md)
- template para resultados reais Canvas: [`docs/15-resultados-canvas.md`](docs/15-resultados-canvas.md)
- kit de screenshots: [`assets/screenshots/README.md`](assets/screenshots/README.md)
- guia Canvas passo a passo: [`docs/04-configuracao-sagemaker-canvas.md`](docs/04-configuracao-sagemaker-canvas.md)

---

# 📁 Dataset escolhido

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

| Campo | Papel planejado |
|---|---|
| `ID_PRODUTO` | Item ID |
| `DATA_EVENTO` | timestamp |
| `PRECO` | coluna adicional/covariável quando suportada pelo fluxo real |
| `FLAG_PROMOCAO` | coluna adicional/covariável quando suportada pelo fluxo real |
| `QUANTIDADE_ESTOQUE` | target |

---

# ☁️ Configuração preparada para o SageMaker Canvas

| Parâmetro | Planejamento |
|---|---|
| Tipo | Time Series Forecasting |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Forecast length | 7 |
| Frequência | diária, conforme detecção/configuração real |
| Colunas adicionais | `PRECO`, `FLAG_PROMOCAO` quando disponíveis no fluxo real |

A interface real do Canvas prevalece sobre este planejamento. Na execução, o projeto registrará exatamente as opções realmente usadas.

**AWS EXECUTION AUTHORIZED = NO**

Nenhum build/prediction pago deve ser iniciado sem autorização explícita e teto financeiro definido.

Guia operacional: [`docs/04-configuracao-sagemaker-canvas.md`](docs/04-configuracao-sagemaker-canvas.md).

---

# 📸 Evidências Canvas pendentes

Após a execução real, somente screenshots reais e sanitizados serão adicionados:

1. `01-canvas-home.png`
2. `02-import-dataset.png`
3. `03-dataset-preview.png`
4. `04-model-configuration.png`
5. `05-training.png`
6. `06-model-analysis.png`
7. `07-feature-importance.png`
8. `08-forecast.png`
9. `09-export.png`

Não publicar Account ID, e-mail, IAM username, access keys, session tokens, ARNs sensíveis, billing pessoal ou URLs assinadas.

---

# 🔎 Gate automático de submissão

O repositório possui um checker local:

```bash
python scripts/check_dio_submission.py
```

Enquanto o Canvas não estiver executado, a saída esperada é:

```text
DIO SUBMISSION READY: NO
```

Depois de inserir todas as evidências reais:

```bash
python scripts/check_dio_submission.py --strict
```

O modo estrito só deve retornar sucesso quando checklist, resultados e nove screenshots reais estiverem completos.

O workflow `DIO readiness` executa a verificação em modo informativo enquanto a pendência AWS é explícita, evitando deixar o CI vermelho apenas porque o Canvas ainda não foi autorizado/executado.

---

# 🐍 Extensão open source opcional — Inventory Forecasting Studio

A extensão Python não substitui o desafio DIO. Ela demonstra uma abordagem reproduzível do mesmo problema com:

- `Naive`, `Drift` e `SeasonalNaive7`;
- AutoGluon TimeSeries 1.6.1;
- 3 folds rolling-origin/expanding-window;
- MAE, RMSE, WAPE, MAPE, WQL e `MACRO_MASE`;
- P10/P50/P90 e calibração;
- diagnóstico por SKU/horizonte;
- Streamlit;
- CI e artifacts auditáveis.

## Resultado agregado dos três folds

| Métrica | AutoGluon | Melhor baseline (`Naive`) |
|---|---:|---:|
| WAPE médio | **0.500177** | 0.739365 |
| RMSE médio | **31.917570** | 45.785757 |
| WQL médio | **0.303370** | 0.647723 |

O `WeightedEnsemble` foi selecionado internamente em 3/3 folds, mas venceu externamente 2/3. No fold 1, `Chronos2` teve WQL melhor. Portanto, o projeto não afirma superioridade universal do ensemble.

Coverage P10–P90 observado: **67,24%**, abaixo de ~80% nominal. Os quantis são nativos, mas não estão perfeitamente calibrados.

Resultados: [`results/validated/`](results/validated/) e [`docs/07-resultados-python.md`](docs/07-resultados-python.md).

---

# 🖥️ Streamlit

```bash
python -m venv .venv
pip install -r requirements-app.txt
streamlit run app.py
```

O Studio apresenta dataset, EDA, benchmarks, estabilidade temporal, calibração e forecast da trilha Python.

---

# 🔐 Segurança

A trilha necessária para preparar/enviar o desafio DIO possui:

- secret-pattern scanning;
- workflows com `contents: read`;
- GitHub Actions oficiais pinadas por commit SHA;
- `DIO submission dependencies` usando `pip-audit` **sem vulnerabilidades ignoradas** nas dependências obrigatórias da aplicação.

A extensão AutoGluon possui dependência transitiva `lightning 2.6.5` afetada por `CVE-2026-58659 / PYSEC-2026-3624`. Em 30/08/2026 ainda não havia release PyPI corrigida compatível. Por isso:

- AutoGluon permanece extensão opcional;
- o fluxo DIO/Canvas não depende de Lightning;
- o audit opcional possui allowlist **somente** para `PYSEC-2026-3624`;
- qualquer novo finding continua falhando o job;
- nenhum checkpoint externo/não confiável é aceito pelo projeto.

Isso é **isolamento e monitoramento de risco**, não alegação de correção upstream.

Veja [`SECURITY.md`](SECURITY.md).

---

# 🧪 Qualidade e CI

A suíte atual possui **25 testes** após a inclusão do readiness checker. A cobertura inclui:

- dataset/cardinalidade;
- unicidade `SKU + data`;
- splits temporais;
- rolling-origin;
- métricas de forecasting/probabilísticas;
- benchmarks;
- contratos AutoGluon;
- UI;
- secret scanner;
- readiness da submissão DIO.

Workflows incluem:

- Dataset validation;
- Python forecasting;
- AutoGluon experiment;
- Streamlit smoke test;
- Security scan;
- DIO readiness.

---

# ⚠️ Limitações

- somente 40 observações por SKU;
- dataset educacional;
- forecast de estoque não equivale a forecast de demanda;
- reposições/reset são intervenções operacionais;
- `PRECO` e `FLAG_PROMOCAO` só são covariáveis futuras válidas se seus valores forem conhecidos no horizonte;
- a extensão Python é demonstrador/portfólio, não sistema production-ready de reposição automática.

---

# 💰 FinOps e cleanup

Custos e estratégia de menor execução estão em:

- [`docs/10-custos-aws.md`](docs/10-custos-aws.md)
- [`docs/12-cleanup-aws.md`](docs/12-cleanup-aws.md)

A execução AWS permanece bloqueada até autorização explícita.

---

# 📋 Antes de enviar para a DIO

- [ ] executar SageMaker Canvas;
- [ ] adicionar os nove screenshots reais e sanitizados;
- [ ] preencher `docs/15-resultados-canvas.md` com resultados reais;
- [ ] documentar métricas/Column impact reais;
- [ ] gerar forecast e export reais;
- [ ] documentar decisão sobre re-treino;
- [ ] escrever conclusões Canvas;
- [ ] confirmar logout/cleanup e revisar billing;
- [ ] reexecutar todos os checks;
- [ ] executar `python scripts/check_dio_submission.py --strict`;
- [ ] somente então mudar `DIO SUBMISSION READY: NO` para `YES` e enviar a URL na plataforma DIO.

**Estado atual: READY AFTER CANVAS — não enviar ainda porque a execução real e as evidências do SageMaker Canvas continuam pendentes.**
