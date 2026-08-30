# Checklist de submissão DIO — SageMaker Canvas

> Baseado no README oficial do desafio `digitalinnovationone/lab-aws-sagemaker-canvas-estoque`, verificado em 30/08/2026.

## Regra de status

- ✅ **PRONTO** = evidência já existe no repositório;
- ⏳ **PENDENTE AWS** = só pode ser concluído com execução real no SageMaker Canvas;
- ❌ **BLOQUEADOR** = impediria a submissão mesmo antes da execução AWS.

## Matriz literal do desafio

| # | Requisito oficial DIO | Status | Evidência / ação |
|---:|---|---|---|
| 1 | Dar fork no projeto | ✅ PRONTO | repositório `matheusflorindo32/lab-aws-sagemaker-canvas-estoque` |
| 2 | Reescrever o README | ✅ PRONTO | `README.md` totalmente reestruturado |
| 3 | Selecionar dataset | ✅ PRONTO | `datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv` |
| 4 | Fazer upload no SageMaker Canvas | ⏳ PENDENTE AWS | capturar `02-import-dataset.png` |
| 5 | Importar dataset no Canvas | ⏳ PENDENTE AWS | capturar `03-dataset-preview.png` |
| 6 | Configurar entrada/saída | ⏳ PENDENTE AWS | target `QUANTIDADE_ESTOQUE`; item `ID_PRODUTO`; timestamp `DATA_EVENTO`; capturar `04-model-configuration.png` |
| 7 | Iniciar treinamento | ⏳ PENDENTE AWS | capturar `05-training.png` |
| 8 | Examinar métricas de performance | ⏳ PENDENTE AWS | registrar somente métricas reais do Canvas em tabela própria |
| 9 | Verificar características principais | ⏳ PENDENTE AWS | capturar `07-feature-importance.png` e documentar sem causalidade indevida |
| 10 | Ajustar/re-treinar se necessário | ⏳ PENDENTE AWS | documentar decisão; não é obrigatório inventar segundo treino se o primeiro for suficiente |
| 11 | Fazer previsão de estoque | ⏳ PENDENTE AWS | capturar `08-forecast.png` |
| 12 | Exportar resultados | ⏳ PENDENTE AWS | salvar export real e capturar `09-export.png` |
| 13 | Analisar previsões | ⏳ PENDENTE AWS | adicionar seção de conclusões baseada no output real |
| 14 | Documentar conclusões/insights | ⏳ PENDENTE AWS | atualizar README após a execução |
| 15 | Enviar URL do repositório na DIO | ⏳ ETAPA FINAL | só depois de fechar itens 4–14 |

## Bloqueadores locais antes da AWS

**Nenhum bloqueador local conhecido no momento.**

O caminho obrigatório da submissão DIO não depende de AutoGluon/Lightning. O workflow de segurança possui gate obrigatório sem vulnerabilidades ignoradas para as dependências usadas no caminho de submissão/aplicação.

A extensão AutoGluon continua no repositório como portfólio e é auditada separadamente; o finding `CVE-2026-58659 / PYSEC-2026-3624` permanece visível e não é mascarado.

## Configuração Canvas preparada

| Campo | Valor |
|---|---|
| Tipo | Time Series Forecasting |
| Dataset | `dataset-1000-com-preco-promocional-e-renovacao-estoque.csv` |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Frequência | Daily |
| Horizonte | 7 dias |
| Covariáveis | `PRECO`, `FLAG_PROMOCAO` |

> Se a interface atual do Canvas não permitir alguma dessas opções exatamente dessa forma, registrar a configuração realmente disponível em vez de forçar a documentação planejada.

## Evidências obrigatórias recomendadas

Salvar em `assets/screenshots/` somente capturas reais e sanitizadas:

1. `01-canvas-home.png`
2. `02-import-dataset.png`
3. `03-dataset-preview.png`
4. `04-model-configuration.png`
5. `05-training.png`
6. `06-model-analysis.png`
7. `07-feature-importance.png`
8. `08-forecast.png`
9. `09-export.png`

Ocultar Account ID, e-mail, IAM username, ARNs sensíveis, billing, tokens, access keys e URLs assinadas.

## Tabela para preencher depois da execução

### Métricas SageMaker Canvas

| Métrica mostrada pelo Canvas | Resultado real |
|---|---|
| WAPE | PENDENTE |
| MAPE | PENDENTE |
| RMSE | PENDENTE |
| MASE | PENDENTE |
| Average wQL / equivalente | PENDENTE |

> Registrar somente as métricas que a interface realmente mostrar. Não inventar métricas ausentes.

### Features / variáveis relevantes

PENDENTE — registrar exatamente o que o Canvas mostrar.

### Forecast exportado

PENDENTE — registrar nome do arquivo/export e síntese dos resultados.

## Checklist pré-envio

- [ ] todos os itens AWS acima concluídos;
- [ ] screenshots reais adicionados e sanitizados;
- [ ] README alterado de `NÃO EXECUTADA` para `EXECUTADA` somente após evidência;
- [ ] métricas Canvas reais documentadas;
- [ ] feature importance real documentada;
- [ ] forecast/export real documentado;
- [ ] conclusões do Canvas documentadas;
- [ ] nenhuma credencial/identificador sensível em commits ou imagens;
- [ ] `Security scan` obrigatório verde;
- [ ] `Dataset validation` verde;
- [ ] revisar custos e fazer logout/cleanup do Canvas;
- [ ] conferir o PR final;
- [ ] somente então enviar a URL na plataforma DIO.

## Decisão atual

**DIO: AINDA NÃO ENVIAR.**

Motivo único relevante: falta a evidência real do fluxo SageMaker Canvas exigido pelo README oficial da DIO. Todo o trabalho local que pode ser preparado sem executar AWS já está organizado para essa etapa.
