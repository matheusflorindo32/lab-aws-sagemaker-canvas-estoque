# Resultados verificados — trilha Python

## Escopo e integridade

Esta página documenta somente resultados realmente executados. A trilha SageMaker Canvas continua separada e **não executada**.

Dataset principal:

`datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv`

- 1.000 registros;
- 25 SKUs;
- 40 observações diárias por SKU;
- horizonte: 7 dias;
- target: `QUANTIDADE_ESTOQUE`;
- covariáveis conhecidas: `PRECO`, `FLAG_PROMOCAO`.

> `QUANTIDADE_ESTOQUE` foi mantida para preservar o problema do desafio DIO. Forecast de estoque observado não equivale a forecast de demanda: resets/reposições são intervenções operacionais que tornam a série mais difícil de interpretar.

---

## Protocolo temporal P1

Além do holdout final 33+7, o projeto executa **3 folds externos rolling-origin/expanding-window** com testes de 7 dias não sobrepostos:

| Fold | Treino por SKU | Teste por SKU |
|---:|---:|---:|
| 1 | 19 | 7 |
| 2 | 26 | 7 |
| 3 | 33 | 7 |

O AutoGluon escolhe o modelo usando somente sua validação interna. O teste externo do fold não é usado para selecionar o modelo.

Dataset SHA-256 registrado no manifesto:

`fe8ffe48cc34cd8540ecba10984066fe503b0bb5ca9d55f9280d5b1960649031`

Configuração:

```text
AutoGluon TimeSeries = 1.6.1
Python = 3.12.14
prediction_length = 7
target = QUANTIDADE_ESTOQUE
freq = D
eval_metric = WQL
quantile_levels = [0.1, 0.5, 0.9]
known_covariates_names = [PRECO, FLAG_PROMOCAO]
random_seed = 123
presets = medium_quality
time_limit = 180 s por fold
```

---

# Benchmarks — robustez em 3 folds

Os baselines são `Naive`, `Drift` e `SeasonalNaive7`. O `Naive` ficou em primeiro entre os baselines nos três folds por WAPE.

| Modelo | WAPE médio | RMSE médio | MACRO_MASE médio | WQL médio | Coverage P10–P90 |
|---|---:|---:|---:|---:|---:|
| **Naive** | **0.739365** | **45.785757** | **2.588005** | **0.647723** | 19.81% |
| Drift | 0.809554 | 52.004579 | 2.853404 | 0.690580 | 23.81% |
| SeasonalNaive7 | 0.874120 | 49.939643 | 3.010651 | 0.818905 | 1.90% |

`MACRO_MASE` significa MASE calculado separadamente por SKU e depois promediado. Não é apresentado como se tivesse a mesma agregação das métricas globais.

Os intervalos empíricos P10–P90 dos benchmarks estão severamente subcalibrados e servem somente como baseline de incerteza.

---

# AutoGluon — resultados fold a fold

O modelo selecionado pela validação interna foi `WeightedEnsemble` em 3/3 folds.

| Fold | Treino/SKU | Modelo selecionado | MAE | RMSE | WAPE | WQL | Coverage P10–P90 |
|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | 19 | WeightedEnsemble | 35.209139 | 40.354636 | 0.700500 | 0.424289 | 54.29% |
| 2 | 26 | WeightedEnsemble | 21.960458 | 28.859860 | 0.441683 | 0.262329 | 81.71% |
| 3 | 33 | WeightedEnsemble | 21.265417 | 26.538214 | 0.358348 | 0.223493 | 65.71% |

### Agregado dos três folds

| Métrica | Média | Mediana | Desvio-padrão |
|---|---:|---:|---:|
| MAE | 26.145005 | 21.960458 | 7.857459 |
| RMSE | 31.917570 | 28.859860 | 7.398349 |
| WAPE | 0.500177 | 0.441683 | 0.178418 |
| WQL | 0.303370 | 0.262329 | 0.106504 |
| Coverage P10–P90 | 67.24% | 65.71% | 13.78 p.p. |

---

## Seleção interna ≠ estabilidade externa

A análise P1 separa duas perguntas diferentes:

1. **Qual modelo a validação interna escolhe?**
2. **Qual modelo realmente vence o teste externo de cada fold?**

| Fold | Selecionado pela validação | Vencedor externo por WQL | Rank externo do WeightedEnsemble | Gap do ensemble para o vencedor |
|---:|---|---|---:|---:|
| 1 | WeightedEnsemble | **Chronos2** | 3 | **27.16% pior em WQL** |
| 2 | WeightedEnsemble | **WeightedEnsemble** | 1 | 0% |
| 3 | WeightedEnsemble | **WeightedEnsemble** | 1 | 0% |

Conclusão:

- `selection_stability = stable`: o WeightedEnsemble foi selecionado internamente em 3/3 folds;
- `external_test_stability = unstable`: venceu 2/3 testes externos, mas caiu para terceiro no fold 1 com degradação material.

Logo, **não é defensável afirmar que o WeightedEnsemble é universalmente o melhor modelo**. A evidência correta é que ele performou melhor em dois dos três testes externos e apresentou sensibilidade relevante à janela com apenas 40 pontos por série.

---

# AutoGluon × melhor baseline

Comparando as médias dos mesmos três folds com o `Naive`:

| Métrica | Naive | AutoGluon selecionado | Redução relativa |
|---|---:|---:|---:|
| WAPE | 0.739365 | **0.500177** | **32.35%** |
| RMSE | 45.785757 | **31.917570** | **30.29%** |
| WQL | 0.647723 | **0.303370** | **53.16%** |

A melhora agregada é substancial neste dataset, mas a variabilidade entre folds impede tratar esse ganho como evidência de produção.

---

# P10 / P50 / P90 — calibração

As previsões AutoGluon possuem quantis nativos. O P1 mediu se esses quantis se comportam como esperado.

### Agregado dos três folds

| Diagnóstico | Observado | Referência nominal |
|---|---:|---:|
| `y <= P10` | 20.95% | ~10% |
| `y <= P50` | 51.05% | ~50% |
| `y <= P90` | 88.19% | ~90% |
| Coverage P10–P90 | **67.24%** | ~80% |
| Largura média P10–P90 | 68.52 | — |
| Quantile crossings | **0** | 0 desejável |

P50 e P90 ficaram relativamente próximos das frequências nominais no agregado, mas P10 ficou alto e o intervalo P10–P90 cobriu somente 67,24% dos valores reais. Portanto, os quantis são úteis para representar incerteza, porém **não estão perfeitamente calibrados**.

### Coverage por horizonte

| h | Coverage | WAPE | WQL | Largura média |
|---:|---:|---:|---:|---:|
| 1 | 61.33% | 0.4685 | 0.2991 | 61.03 |
| 2 | 58.67% | 0.5905 | 0.3610 | 64.99 |
| 3 | 61.33% | 0.5460 | 0.3289 | 69.91 |
| 4 | 69.33% | 0.4934 | 0.2973 | 68.48 |
| 5 | 73.33% | 0.4451 | 0.2672 | 70.87 |
| 6 | 77.33% | 0.4010 | 0.2481 | 72.72 |
| 7 | 69.33% | 0.5273 | 0.3061 | 71.67 |

A largura tende a aumentar nos horizontes mais distantes, mas o coverage não piora monotonicamente. Com somente 75 observações por passo de horizonte, essa análise é **exploratória**.

---

# Diagnóstico por SKU

Usando MAE médio dos três folds:

### Cinco mais previsíveis

| SKU | MAE médio | WAPE médio | MACRO_MASE médio | Coverage |
|---|---:|---:|---:|---:|
| 1011 | **16.0186** | 0.2954 | 0.8914 | 95.24% |
| 1013 | 19.7747 | 0.3405 | 1.2209 | 80.95% |
| 1005 | 20.8032 | 0.3843 | 1.1781 | 90.48% |
| 1022 | 20.9321 | 0.4100 | 1.2887 | 80.95% |
| 1024 | 21.1586 | 0.3709 | 1.1897 | 71.43% |

### Cinco menos previsíveis

| SKU | MAE médio | WAPE médio | MACRO_MASE médio | Coverage |
|---|---:|---:|---:|---:|
| 1006 | **33.2197** | 0.9832 | 2.6026 | 38.10% |
| 1008 | 32.3849 | 0.9017 | 2.6394 | 61.90% |
| 1004 | 30.9993 | 0.4982 | 1.8851 | 42.86% |
| 1002 | 29.6194 | 1.0024 | 2.0344 | 57.14% |
| 1015 | 29.1400 | 0.6870 | 2.0056 | 57.14% |

Essas diferenças são descritivas. O dataset é pequeno demais para concluir causalidade entre dificuldade de previsão e preço, promoção ou resets.

---

# Holdout final e feature importance

No fold final (33+7), o leaderboard de teste continua:

| Rank | Modelo | WQL loss |
|---:|---|---:|
| 1 | WeightedEnsemble | **0.223493** |
| 2 | DirectTabular | 0.228474 |
| 3 | Chronos2 | 0.265239 |
| 4 | Toto2 | 0.283392 |
| 5 | RecursiveTabular | 0.407835 |
| 6 | SeasonalNaive | 0.416962 |
| 7 | ETS | 0.448723 |
| 8 | Theta | 0.480026 |

Feature importance no holdout final:

| Variável | Importance |
|---|---:|
| `PRECO` | 0.000169 |
| `FLAG_PROMOCAO` | -0.000625 |

Ambas ficaram próximas de zero; não há interpretação causal.

---

# Evidências permanentes

Resultados pequenos e auditáveis estão em [`../results/validated/`](../results/validated/):

- `autogluon_multifold_metrics.csv`;
- `autogluon_multifold_summary.csv`;
- `model_stability.csv`;
- `horizon_calibration.csv`;
- `sku_metrics.csv`;
- `autogluon_multifold_manifest.json`;
- `benchmark_multifold_summary.csv`.

O manifesto registra o hash do dataset e a proveniência do workflow/artifact. As previsões completas continuam regeneráveis pelo script e preservadas no artifact de Actions; modelos/checkpoints não são versionados.

### Reprodução

```bash
pip install -r requirements-ml.txt
python scripts/train_autogluon.py --time-limit 180 --presets medium_quality
python scripts/train_autogluon_multifold.py --time-limit 180 --presets medium_quality
```

---

# Limitações que permanecem

- somente 40 observações por SKU;
- primeiro fold possui somente 19 observações de treino;
- três folds são melhores que um holdout único, mas ainda constituem pouca evidência temporal;
- dados educacionais/sintéticos;
- resets/reposições misturam dinâmica de estoque com decisões operacionais;
- ausência de demanda/vendas explícitas;
- preço e promoção precisam ser realmente conhecidos no horizonte futuro para uso como `known_covariates`;
- quantis apresentam subcoverage;
- estabilidade externa do ensemble é limitada;
- o sistema não é política automática de reposição nem produto production-ready.
