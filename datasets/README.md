# Datasets

Este diretório preserva os datasets originais fornecidos no desafio da DIO.

## Dataset principal selecionado

`dataset-1000-com-preco-promocional-e-renovacao-estoque.csv`

Schema esperado:

| Campo | Papel no modelo | Descrição |
|---|---|---|
| `ID_PRODUTO` | Item ID | Identificador do produto/SKU |
| `DATA_EVENTO` | Timestamp | Data da observação |
| `PRECO` | Covariável | Preço observado do produto |
| `FLAG_PROMOCAO` | Covariável | Indicador binário de promoção |
| `QUANTIDADE_ESTOQUE` | Target | Quantidade disponível em estoque |

O dataset principal possui 1.000 registros, 25 SKUs (`1000` a `1024`) e observações diárias entre 2023-12-31 e 2024-02-08.

## Política de preservação

Os arquivos originais da DIO não devem ser sobrescritos. Qualquer enriquecimento futuro deve ser salvo em `datasets/enriched/` com origem, transformação e objetivo documentados.

## Limitação importante

Este é um dataset educacional e de curta duração. Forecast de estoque não deve ser interpretado automaticamente como forecast de demanda. Em um sistema corporativo, vendas, demanda, lead time, nível de serviço, estoque de segurança e custos de ruptura/armazenagem também deveriam ser considerados.
