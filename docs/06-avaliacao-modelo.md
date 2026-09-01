# Avaliação do Modelo de Forecasting

> Status: **PENDENTE DE EXECUÇÃO NO AMAZON SAGEMAKER CANVAS**. Este documento define como interpretar métricas sem fabricar resultados.

## Métricas de erro

Nem toda interface/configuração do Canvas necessariamente exibirá todas as métricas abaixo. O projeto registrará somente os valores realmente apresentados na execução.

### WAPE — Weighted Absolute Percentage Error

Resume o erro absoluto total em relação ao volume total observado. Em geral, valores menores indicam melhor ajuste. É útil para comparar erro relativo agregado, mas pode esconder diferenças importantes entre SKUs individuais.

### MAPE — Mean Absolute Percentage Error

Calcula o erro percentual absoluto médio. É intuitivo em termos percentuais, porém pode se tornar instável ou pouco informativo quando os valores reais são iguais ou próximos de zero.

### RMSE — Root Mean Squared Error

Penaliza erros maiores de forma mais intensa por elevar os resíduos ao quadrado antes de calcular a raiz. É expresso na escala da variável-alvo e, por isso, deve ser interpretado considerando a magnitude típica de `QUANTIDADE_ESTOQUE`.

### MASE — Mean Absolute Scaled Error

Compara o erro do modelo com uma referência ingênua (naive) de previsão. Como regra interpretativa geral:

- `MASE < 1`: o modelo supera a referência ingênua usada no escalonamento;
- `MASE = 1`: desempenho semelhante à referência;
- `MASE > 1`: a referência ingênua apresenta desempenho melhor.

A interpretação final depende de como a métrica foi calculada na execução utilizada.

### Average wQL — Average Weighted Quantile Loss

Avalia previsões probabilísticas em diferentes quantis e penaliza de forma assimétrica previsões acima ou abaixo do observado conforme o quantil analisado. É especialmente útil quando o objetivo não é apenas uma previsão pontual, mas também representar incerteza.

## Tabela de resultados

| Métrica | Resultado | Interpretação |
|---|---:|---|
| WAPE | PENDENTE | aguardando execução real no Canvas |
| MAPE | PENDENTE | aguardando execução real no Canvas |
| RMSE | PENDENTE | aguardando execução real no Canvas |
| MASE | PENDENTE | aguardando execução real no Canvas |
| Average wQL | PENDENTE | aguardando execução real no Canvas |

## Regra de decisão

Nenhuma métrica será usada isoladamente para declarar que o modelo é “bom”. A avaliação deverá considerar:

1. métricas realmente disponibilizadas pelo Canvas;
2. erro por SKU quando disponível;
3. comportamento dos resíduos/previsões;
4. incerteza do forecast;
5. utilidade operacional no contexto do Lab;
6. limitações do dataset curto e educacional.

## Feature importance / impact

Quando a interface fornecer impacto/importância de variáveis, registrar somente os valores observados. O foco será verificar se `PRECO`, `FLAG_PROMOCAO` e componentes temporais disponíveis contribuem para a previsão.

Importância de variável não deve ser interpretada automaticamente como causalidade.

## Quantis e intervalos

Se a execução fornecer quantis como P10, P50 ou P90, eles poderão ser usados para representar cenários de incerteza. Os valores somente serão adicionados após exportação ou captura verificável do Canvas.
