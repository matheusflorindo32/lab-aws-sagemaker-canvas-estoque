# Changelog

## Unreleased

### Added
- Estrutura profissional de documentação para o desafio DIO.
- Baseline de segurança para evitar exposição de credenciais AWS.
- Scanner de segredos em Python com workflow dedicado de segurança.
- Script de validação do dataset sem dependências externas.
- Testes unitários para validação, EDA, segurança e forecasting.
- Análise exploratória descritiva reproduzível com resultados verificados em CI.
- Workflow de CI para compilar scripts, executar testes, validar o dataset e rodar a EDA.
- Guia de execução no Amazon SageMaker Canvas.
- Guia de interpretação de métricas de forecasting.
- Checklist de evidências/sanitização de screenshots AWS.
- Documentação de custos e cleanup AWS.
- Política de integridade dos resultados.
- Guia de contribuição.
- `Inventory Forecasting Studio` em Streamlit com EDA, benchmarks, leaderboard, forecast por SKU, quantis e export CSV.
- Núcleo de forecasting multi-SKU com holdout temporal de 7 dias.
- Métricas MAE, RMSE, WAPE, MAPE, MASE e WQL implementadas e testadas.
- Benchmarks `Naive`, `SeasonalNaive7` e `Drift`.
- Quantis empíricos P10/P50/P90 para os benchmarks leves, explicitamente separados dos quantis nativos de AutoML.
- Integração opcional com AutoGluon TimeSeries 1.6.x, WQL, P10/P50/P90 e covariáveis conhecidas.
- Workflow `Python forecasting` com geração e verificação de 525 previsões de holdout.
- Workflow isolado para experimento AutoGluon com artefatos de avaliação.
- Resultados reais dos benchmarks versionados em `results/metrics/` e `results/exports/`.
- Documentação da trilha open source em `docs/05-implementacao-python.md`, `docs/07-resultados-python.md` e `docs/08-inventory-forecasting-studio.md`.

### Changed
- README reestruturado para apresentar o Lab como case de portfólio, preservando o objetivo original de previsão de estoque.
- Validação do dataset ampliada para cardinalidade, preço negativo, chave `SKU + data`, regularidade temporal e domínio dos campos.
- `.gitignore` ajustado para restringir padrões AWS sem ignorar genericamente qualquer arquivo `config`.
- Arquitetura do projeto ampliada para separar claramente a trilha original SageMaker Canvas da trilha Python realmente executada.
- Status experimental agora diferencia benchmarks reproduzidos, AutoGluon executado quando houver artefatos e Canvas não executado.
