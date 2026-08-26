# Resultados verificados — trilha Python

## Protocolo

Os resultados abaixo foram produzidos pelo workflow `Python forecasting` em GitHub Actions com Python 3.12, usando holdout temporal dos últimos 7 dias de cada SKU.

- dataset: 1.000 registros;
- SKUs: 25;
- treino por SKU: 33 observações;
- holdout por SKU: 7 observações;
- observações avaliadas por modelo: 175;
- modelos benchmark: 3;
- linhas de forecast verificadas: 525.

## Leaderboard dos benchmarks

| Rank | Modelo | MAE | RMSE | WAPE | MAPE | MASE | WQL |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Naive | 42.828571 | 50.790944 | 0.721714 | 1.261017 | 2.837697 | 0.662766 |
| 2 | SeasonalNaive7 | 44.045714 | 48.260010 | 0.742224 | 2.417650 | 2.849374 | 0.718580 |
| 3 | Drift | 47.422143 | 56.697834 | 0.799121 | 1.145737 | 3.164879 | 0.709079 |

O ranking primário do Studio utiliza WAPE, com RMSE como desempate.

## Interpretação

O `Naive` foi o melhor dos três benchmarks simples em WAPE, mas os resultados são fracos em termos absolutos:

- WAPE de aproximadamente 72,17% indica erro absoluto agregado elevado em relação ao volume real observado;
- MASE acima de 1 em todos os modelos indica que nenhum desses benchmarks superou de forma consistente a referência naïve de um passo usada na escala;
- o comportamento de renovação do estoque, com saltos periódicos para níveis altos, é uma fonte importante de descontinuidade e torna a extrapolação simples difícil;
- `SeasonalNaive7` apresentou RMSE menor que o `Naive`, mas WAPE, MAPE, MASE e WQL piores;
- `Drift` não foi competitivo nesse holdout.

Esses resultados não demonstram que AutoGluon será necessariamente bom; demonstram apenas que há espaço real para modelos mais expressivos e que qualquer ganho precisa ser comprovado no mesmo holdout.

## P10/P50/P90

Nos benchmarks leves, P10/P50/P90 são intervalos empíricos baseados nas inovações históricas e **não** devem ser confundidos com quantis probabilísticos nativos do AutoGluon.

## Artefatos

Resultados versionados:

- `results/metrics/benchmark_metrics.csv`;
- `results/exports/benchmark_leaderboard.csv`.

O CSV completo com 525 previsões foi produzido e verificado pelo GitHub Actions e preservado como artefato `inventory-forecasting-benchmarks`.

## AutoGluon

A seção AutoGluon só deve receber números depois que o workflow `AutoGluon experiment` concluir com sucesso e os artefatos forem inspecionados. Em caso de falha de instalação, treino ou avaliação, o status permanece **NÃO EXECUTADO / FALHOU**, sem preenchimento artificial.
