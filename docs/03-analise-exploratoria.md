# Análise Exploratória Descritiva

Esta análise usa apenas a biblioteca padrão do Python e pode ser reproduzida com:

```bash
python scripts/analyze_dataset.py
```

> As estatísticas abaixo foram obtidas no GitHub Actions a partir do dataset oficial selecionado. Elas são **descritivas** e não demonstram causalidade entre preço, promoção e nível de estoque.

## Integridade do baseline

A validação automatizada confirmou:

- 1.000 registros;
- 25 SKUs;
- 40 observações por SKU;
- período de 2023-12-31 a 2024-02-08;
- 0 linhas com campos ausentes;
- 0 duplicatas exatas;
- 0 chaves `ID_PRODUTO + DATA_EVENTO` duplicadas;
- 0 pontos diários ausentes nas séries;
- 0 linhas inválidas.

## Estatísticas descritivas

| Indicador | Resultado |
|---|---:|
| Registros | 1.000 |
| SKUs | 25 |
| Preço médio | 78,64 |
| Preço mínimo | 18,31 |
| Preço máximo | 187,04 |
| Estoque médio | 55,73 |
| Estoque mínimo | 1 |
| Estoque máximo | 100 |
| Registros promocionais | 20,60% |
| Estoque médio em promoção | 57,93 |
| Estoque médio sem promoção | 55,15 |

## Volatilidade descritiva do estoque

Top 5 SKUs pelo desvio-padrão populacional da quantidade em estoque:

| SKU | Desvio-padrão |
|---|---:|
| 1003 | 32,13 |
| 1009 | 32,12 |
| 1018 | 31,90 |
| 1024 | 31,66 |
| 1017 | 31,55 |

Esses valores ajudam a identificar produtos com maior variação histórica no período observado, mas não constituem forecast nem recomendação automática de reposição.

## Interpretação responsável

O estoque médio observado nos registros promocionais foi numericamente maior que o estoque médio nos registros não promocionais. Isso **não permite concluir** que promoções aumentam estoque, reduzem demanda ou causam qualquer outro efeito. O dataset pode conter reposições, padrões específicos por SKU e outros fatores não modelados.

A avaliação de `PRECO` e `FLAG_PROMOCAO` como variáveis explicativas será feita no SageMaker Canvas e só será documentada como resultado do modelo após a execução real.
