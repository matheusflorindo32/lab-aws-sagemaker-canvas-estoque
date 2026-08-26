# Configuração do Amazon SageMaker Canvas

> Status: **PENDENTE DE EXECUÇÃO NA AWS**. Este documento prepara a etapa prática sem inventar resultados.

## Antes de começar

- confirme que está usando a conta AWS correta;
- consulte [`10-custos-aws.md`](10-custos-aws.md);
- evite credenciais administrativas quando não forem necessárias;
- prepare o dataset já validado pelo workflow do projeto.

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
12. Após o treinamento, registre somente as métricas realmente exibidas pelo Canvas.
13. Analise a importância/impacto das variáveis disponibilizada pela interface.
14. Gere previsões para um ou mais SKUs.
15. Exporte os resultados em CSV quando disponível.
16. Salve apenas screenshots reais e sanitizados.
17. Ao concluir, siga [`12-cleanup-aws.md`](12-cleanup-aws.md).

## Evidências a coletar

Salve as imagens em `assets/screenshots/` usando:

1. `01-canvas-home.png`
2. `02-import-dataset.png`
3. `03-dataset-preview.png`
4. `04-model-configuration.png`
5. `05-training.png`
6. `06-model-analysis.png`
7. `07-feature-importance.png`
8. `08-forecast.png`
9. `09-export.png`

Consulte também [`../assets/screenshots/README.md`](../assets/screenshots/README.md).

## Resultados a registrar

Preencha somente com dados reais do Canvas:

| Métrica | Resultado |
|---|---|
| WAPE | PENDENTE |
| MAPE | PENDENTE |
| RMSE | PENDENTE |
| MASE | PENDENTE |
| Average wQL | PENDENTE |

Nem toda execução/interface exibe necessariamente todas as métricas acima. Registre apenas as métricas efetivamente apresentadas no seu modelo. Os critérios de interpretação estão em [`06-avaliacao-modelo.md`](06-avaliacao-modelo.md).

## Destinos dos resultados

- métricas: `results/metrics/`;
- forecasts: `results/predictions/`;
- exports auxiliares: `results/exports/`.

## Checklist de segurança antes do commit

- [ ] nenhum Access Key ID;
- [ ] nenhum Secret Access Key;
- [ ] nenhum Session Token;
- [ ] nenhum e-mail pessoal desnecessário;
- [ ] nenhum Account ID desnecessário;
- [ ] nenhum ARN ou usuário IAM sensível;
- [ ] nenhuma informação privada de billing.
