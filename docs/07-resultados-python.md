# Resultados verificados — trilha Python

## Protocolo

Os resultados abaixo foram produzidos em GitHub Actions com Python 3.12, usando holdout temporal dos últimos 7 dias de cada SKU.

- dataset: 1.000 registros;
- SKUs: 25;
- treino por SKU: 33 observações;
- holdout por SKU: 7 observações;
- observações reais de teste: 175;
- horizonte: 7 dias;
- frequência: diária.

## Benchmarks leves

O workflow `Python forecasting` executou três referências transparentes. Para cada modelo foram produzidas 175 previsões; o artefato contém 525 linhas no total.

| Rank | Modelo | MAE | RMSE | WAPE | MAPE | MASE | WQL |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Naive | 42.828571 | 50.790944 | 0.721714 | 1.261017 | 2.837697 | 0.662766 |
| 2 | SeasonalNaive7 | 44.045714 | 48.260010 | 0.742224 | 2.417650 | 2.849374 | 0.718580 |
| 3 | Drift | 47.422143 | 56.697834 | 0.799121 | 1.145737 | 3.164879 | 0.709079 |

O `Naive` foi o melhor baseline por WAPE, mas o erro ainda é elevado. MASE acima de 1 nos três modelos reforça que esses métodos simples não descrevem bem as descontinuidades de renovação do estoque.

## AutoGluon TimeSeries 1.6.1 — execução real

O workflow `AutoGluon experiment` instalou AutoGluon TimeSeries 1.6.1 e treinou o modelo no GitHub Actions, sem GPU, com 4 CPUs.

Configuração efetivamente usada:

```text
prediction_length = 7
target = QUANTIDADE_ESTOQUE
freq = D
eval_metric = WQL
quantile_levels = [0.1, 0.5, 0.9]
known_covariates_names = [PRECO, FLAG_PROMOCAO]
random_seed = 123
presets = medium_quality
time_limit = 180 s
```

O treino utilizou 825 observações, correspondentes a 33 dias × 25 SKUs. O holdout permaneceu formado pelos 7 dias finais de cada SKU.

### Modelos treinados

- SeasonalNaive;
- RecursiveTabular;
- DirectTabular;
- ETS;
- Theta;
- Chronos2;
- Toto2;
- WeightedEnsemble.

O AutoGluon concluiu o treinamento em aproximadamente **11,99 s** após a instalação das dependências.

### Leaderboard de teste — WQL

O AutoGluon representa métricas de perda com sinal invertido para obedecer à convenção interna `higher_is_better`. Na tabela abaixo é apresentada também a magnitude positiva da perda, em que **menor é melhor**.

| Rank | Modelo | score_test bruto | WQL loss |
|---:|---|---:|---:|
| 1 | WeightedEnsemble | -0.223493 | 0.223493 |
| 2 | DirectTabular | -0.228474 | 0.228474 |
| 3 | Chronos2 | -0.265239 | 0.265239 |
| 4 | Toto2 | -0.283392 | 0.283392 |
| 5 | RecursiveTabular | -0.407835 | 0.407835 |
| 6 | SeasonalNaive | -0.416962 | 0.416962 |
| 7 | ETS | -0.448723 | 0.448723 |
| 8 | Theta | -0.480026 | 0.480026 |

O melhor modelo foi o **WeightedEnsemble**.

Pesos registrados pelo AutoGluon:

| Componente | Peso |
|---|---:|
| DirectTabular | 0.81 |
| Toto2 | 0.12 |
| Chronos2 | 0.05 |
| RecursiveTabular | 0.02 |

### Métricas independentes do melhor modelo

As 175 previsões exportadas pelo `WeightedEnsemble` foram reconciliadas com os valores reais do mesmo holdout. As métricas abaixo foram recalculadas independentemente a partir do arquivo de previsões:

| Métrica | Resultado |
|---|---:|
| MAE | 21.265417 |
| RMSE | 26.538214 |
| WAPE | 0.358348 |
| MAPE | 1.472072 |
| WQL | 0.223493 |

A reprodução independente do WQL resultou em `0.22349288237753498`, consistente com a magnitude do score bruto `-0.22349288237753495` retornado por `predictor.evaluate()`.

### Comparação com o melhor baseline

| Métrica | Naive | AutoGluon WeightedEnsemble |
|---|---:|---:|
| MAE | 42.828571 | 21.265417 |
| RMSE | 50.790944 | 26.538214 |
| WAPE | 0.721714 | 0.358348 |
| WQL | 0.662766 | 0.223493 |

No holdout utilizado, o AutoGluon apresentou redução substancial do erro em relação ao melhor baseline simples. Isso é evidência válida **apenas para este dataset e este protocolo de backtest**; não implica desempenho de produção nem generalização para outros períodos.

## Feature importance das covariáveis

O AutoGluon calculou:

| Variável | Importance |
|---|---:|
| `PRECO` | 0.000169 |
| `FLAG_PROMOCAO` | -0.000625 |

Os valores estão muito próximos de zero. Portanto, nesta execução, não há evidência de que essas duas covariáveis tenham contribuído materialmente para o desempenho do ensemble. Importância negativa de `FLAG_PROMOCAO` não deve ser interpretada como causalidade; indica apenas que, no procedimento de permutação/avaliação utilizado, sua presença não melhorou o score observado.

## P10 / P50 / P90

O AutoGluon produziu quantis probabilísticos nativos `0.1`, `0.5` e `0.9` para cada um dos 175 pontos do holdout.

Nos benchmarks leves, P10/P50/P90 continuam sendo intervalos empíricos baseados nas inovações históricas e **não** devem ser confundidos com os quantis nativos do AutoGluon.

## Artefatos

Versionados:

- `results/metrics/benchmark_metrics.csv`;
- `results/exports/benchmark_leaderboard.csv`;
- `results/autogluon/leaderboard.csv`;
- `results/autogluon/evaluation.txt`;
- `results/autogluon/feature_importance.csv`;
- `results/autogluon/metrics_summary.csv`.

Preservados como artefatos do GitHub Actions:

- `inventory-forecasting-benchmarks` — previsões completas dos três benchmarks;
- `inventory-forecasting-autogluon` — leaderboard, 175 previsões com mean/P10/P50/P90, avaliação e feature importance.

## Limitações

- apenas 40 observações por SKU;
- somente um holdout de 7 dias;
- dados educacionais/sintéticos;
- forte presença de resets de estoque;
- ausência de demanda/vendas explícitas;
- covariáveis futuras de preço/promoção precisam ser fornecidas explicitamente em uma previsão genuinamente futura;
- o modelo não deve ser tratado como política automática de reposição.
