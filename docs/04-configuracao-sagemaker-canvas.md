# Configuração do Amazon SageMaker Canvas

> Status: **PENDENTE DE EXECUÇÃO NA AWS**. Este documento prepara a etapa prática sem inventar resultados.

## Configuração do modelo

Use o dataset:

`datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv`

Configuração recomendada para a primeira execução:

| Parâmetro | Valor |
|---|---|
| Tipo de problema | Time Series Forecasting |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Frequência | Daily |
| Horizonte inicial | 7 dias |
| Covariáveis | `PRECO`, `FLAG_PROMOCAO` |

## Passo a passo

1. Acesse a conta AWS destinada ao Lab.
2. Abra o Amazon SageMaker e entre no SageMaker Canvas.
3. Importe o CSV principal.
4. Confira se o schema e os tipos foram reconhecidos corretamente.
5. Crie um novo modelo de previsão de séries temporais.
6. Defina `QUANTIDADE_ESTOQUE` como target.
7. Defina `ID_PRODUTO` como identificador dos itens.
8. Defina `DATA_EVENTO` como timestamp.
9. Configure frequência diária e horizonte inicial de 7 dias.
10. Revise `PRECO` e `FLAG_PROMOCAO` como variáveis explicativas quando o fluxo do Canvas permitir.
11. Inicie o treinamento.
12. Após o treinamento, registre as métricas exibidas pelo Canvas.
13. Analise a importância/impacto das variáveis disponibilizada pela interface.
14. Gere previsões para um ou mais SKUs.
15. Exporte os resultados em CSV quando disponível.
16. Salve apenas screenshots sanitizados.

## Evidências a coletar

Salve as imagens em `assets/screenshots/` usando, preferencialmente:

- `01-import-dataset.png`
- `02-dataset-preview.png`
- `03-model-configuration.png`
- `04-training.png`
- `05-model-analysis.png`
- `06-feature-impact.png`
- `07-forecast.png`

## Resultados a registrar

Preencha somente com dados reais do Canvas:

| Métrica | Resultado |
|---|---|
| WAPE | PENDENTE |
| MAPE | PENDENTE |
| RMSE | PENDENTE |
| MASE | PENDENTE |
| Average wQL | PENDENTE |

Nem toda execução/interface exibe necessariamente todas as métricas acima. Registre apenas as métricas efetivamente apresentadas no seu modelo.

## Checklist de segurança antes do commit

- nenhum Access Key ID;
- nenhum Secret Access Key;
- nenhum Session Token;
- nenhum e-mail pessoal desnecessário;
- nenhum Account ID desnecessário;
- nenhum ARN ou usuário IAM sensível;
- nenhuma informação privada de billing.
