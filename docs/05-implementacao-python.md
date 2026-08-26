# Implementação open source em Python

## Status

**EXECUTADO** para validação, EDA e benchmarks leves.  
**AutoGluon TimeSeries:** executado somente quando houver artefatos reais em `results/autogluon/`; nunca inferir resultados a partir da configuração.

## Por que existe esta trilha

O desafio original da DIO propõe Amazon SageMaker Canvas. Este repositório preserva essa trilha e o guia de execução, mas também implementa uma alternativa open source para tornar o experimento reproduzível sem depender de custos de infraestrutura AWS.

A implementação Python mantém o mesmo problema de negócio:

- Item ID: `ID_PRODUTO`;
- timestamp: `DATA_EVENTO`;
- target: `QUANTIDADE_ESTOQUE`;
- frequência: diária;
- horizonte: 7 dias;
- covariáveis planejadas para AutoGluon: `PRECO`, `FLAG_PROMOCAO`.

## Validação temporal

Para cada um dos 25 SKUs:

1. as observações são ordenadas por data;
2. os últimos 7 dias são separados como holdout;
3. os 33 dias anteriores formam o histórico de treino;
4. nenhuma observação do target no holdout entra no treino.

Isso produz 175 observações reais de teste por modelo (25 SKUs × 7 dias).

## Benchmarks leves

Três referências transparentes são executadas sem dependências externas:

- `Naive`: repete a última observação de treino;
- `SeasonalNaive7`: repete os últimos 7 valores do histórico;
- `Drift`: extrapola a tendência linear entre primeira e última observação do treino.

As métricas calculadas são MAE, RMSE, WAPE, MAPE, MASE e WQL.

### Quantis nos benchmarks

Os P10/P50/P90 dos benchmarks leves **não são quantis nativos de um modelo probabilístico**. Eles são construídos de forma transparente a partir dos quantis empíricos das inovações de um passo no histórico e adicionados ao point forecast, com piso em zero.

Essa abordagem serve apenas como baseline de incerteza. Quando AutoGluon é executado, seus quantis são probabilísticos e nativos do `TimeSeriesPredictor`.

## Execução

```bash
python scripts/validate_dataset.py
python scripts/run_benchmarks.py
```

O benchmark gera:

```text
results/metrics/benchmark_metrics.csv
results/predictions/benchmark_holdout_predictions.csv
results/exports/benchmark_leaderboard.csv
```

No GitHub Actions, o CSV completo de previsões também é preservado como artefato do workflow `Python forecasting`.

## AutoGluon TimeSeries

Instalação:

```bash
pip install -r requirements-ml.txt
```

Execução sugerida:

```bash
python scripts/train_autogluon.py --time-limit 300 --presets medium_quality
```

Configuração:

```text
prediction_length = 7
freq = D
eval_metric = WQL
quantile_levels = [0.1, 0.5, 0.9]
known_covariates_names = [PRECO, FLAG_PROMOCAO]
```

No backtest histórico, preço e promoção do holdout são conhecidos e podem ser fornecidos ao modelo sem expor o target futuro. Para uma previsão realmente futura, valores de `PRECO` e `FLAG_PROMOCAO` precisam vir de um cenário/plano comercial explícito; o código não inventa essas covariáveis.
