# Matriz de evidências DIO — SageMaker Canvas

> Fonte de rastreabilidade entre o requisito oficial, a evidência esperada e o ponto em que ela aparecerá no repositório. Nenhuma evidência AWS é marcada como concluída antes de execução real.

| ID | Requisito DIO | Screenshot | Arquivo / evidência | Texto no README | Status |
|---:|---|---|---|---|---|
| 1 | Fork do projeto | — | URL do repositório | abertura/objetivo | PASS |
| 2 | README reescrito | — | `README.md` | documento principal | PASS |
| 3 | Dataset selecionado | — | `datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv` | seção Dataset | PASS |
| 4 | Upload no Canvas | `02-import-dataset.png` | Canvas import real | seção Execução Canvas | PENDING AWS |
| 5 | Dataset importado/validado no Canvas | `03-dataset-preview.png` | preview/schema real | seção Execução Canvas | PENDING AWS |
| 6 | Variáveis/configuração | `04-model-configuration.png` | target/item ID/timestamp/horizon reais | seção Configuração Canvas | PENDING AWS |
| 7 | Treinamento iniciado/concluído | `05-training.png` | modelo Canvas real | seção Execução Canvas | PENDING AWS |
| 8 | Métricas de performance | `06-model-analysis.png` | `docs/15-resultados-canvas.md` | seção Resultados Canvas | PENDING AWS |
| 9 | Características/column impact | `07-feature-importance.png` | `docs/15-resultados-canvas.md` | seção Resultados Canvas | PENDING AWS |
| 10 | Ajustar/re-treinar se necessário | — | decisão documentada em `docs/15-resultados-canvas.md` | conclusões | PENDING AWS |
| 11 | Fazer previsão de estoque | `08-forecast.png` | previsão real do Canvas | seção Forecast | PENDING AWS |
| 12 | Exportar resultados | `09-export.png` | export real em `results/exports/` quando disponível | seção Forecast/Export | PENDING AWS |
| 13 | Analisar previsões | `08-forecast.png` | `docs/15-resultados-canvas.md` | conclusões | PENDING AWS |
| 14 | Documentar conclusões/insights | — | `docs/15-resultados-canvas.md` | conclusões finais | PENDING AWS |
| 15 | Enviar URL na plataforma DIO | — | URL final do repositório | — | PENDING AWS |

## Evidência de contexto

`01-canvas-home.png` é recomendado como evidência de contexto da sessão, mas não substitui nenhum dos requisitos funcionais acima.

## Regra de integridade

- screenshots devem ser reais;
- métricas devem ser copiadas da interface/export real;
- não reutilizar números da trilha Python como se fossem Canvas;
- não criar arquivos vazios apenas para fazer o readiness checker passar;
- sanitizar Account ID, e-mail, IAM username, ARNs sensíveis, billing, tokens e URLs assinadas.

## Gate atual

**DIO SUBMISSION READY: NO**

Motivo: requisitos 4–14 ainda dependem da execução real do SageMaker Canvas.
