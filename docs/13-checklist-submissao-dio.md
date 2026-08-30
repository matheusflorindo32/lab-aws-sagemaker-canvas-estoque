# Checklist de submissão DIO — SageMaker Canvas

> Fonte de verdade para decidir se o repositório pode ser enviado à DIO. Rubrica reconstruída a partir do README oficial `digitalinnovationone/lab-aws-sagemaker-canvas-estoque`, revalidado em 30/08/2026.

## Status permitidos

- `PASS` — requisito comprovado no repositório;
- `PENDING AWS` — depende de execução real no SageMaker Canvas;
- `FAIL` — requisito deveria estar concluído, mas há problema local;
- `NOT REQUIRED` — melhoria opcional/condicional, sem obrigação de execução quando não aplicável.

## Rubrica literal reconstruída

| ID | Categoria | Requisito DIO | Obrigatório? | Evidência esperada | Status atual | Ação restante |
|---:|---|---|---|---|---|---|
| 1 | explícito | Dar fork no projeto | sim | repositório derivado do Lab | PASS | — |
| 2 | explícito | Reescrever o README | sim | `README.md` próprio | PASS | — |
| 3 | explícito | Selecionar dataset | sim | CSV escolhido em `datasets/` | PASS | — |
| 4 | explícito | Fazer upload/import do dataset no SageMaker Canvas | sim | `02-import-dataset.png` + `03-dataset-preview.png` | PENDING AWS | executar import real |
| 5 | explícito | Configurar variáveis de entrada e saída | sim | `04-model-configuration.png` | PENDING AWS | registrar configuração real |
| 6 | explícito | Iniciar treinamento do modelo | sim | `05-training.png` | PENDING AWS | executar build real |
| 7 | explícito | Examinar métricas de performance | sim | `06-model-analysis.png` + `docs/15-resultados-canvas.md` | PENDING AWS | copiar somente métricas reais |
| 8 | explícito | Verificar características que influenciam previsões | sim | `07-feature-importance.png` / Column impact | PENDING AWS | registrar somente output real |
| 9 | condicional | Ajustar/re-treinar se necessário | somente se necessário | decisão documentada | PENDING AWS | decidir depois de analisar o primeiro build |
| 10 | explícito | Fazer previsões de estoque | sim | `08-forecast.png` | PENDING AWS | gerar previsão real |
| 11 | explícito | Exportar resultados | sim | `09-export.png` + export real quando apropriado | PENDING AWS | executar export |
| 12 | explícito | Analisar previsões | sim | `docs/15-resultados-canvas.md` | PENDING AWS | escrever análise baseada no output real |
| 13 | explícito | Documentar conclusões/insights | sim | README + resultados Canvas | PENDING AWS | concluir após execução |
| 14 | explícito | Enviar URL do repositório na plataforma DIO | sim | URL final | PENDING AWS | somente após fechar itens anteriores |
| 15 | melhoria | Extensão Python/AutoGluon | não | `results/validated/`, docs e CI | NOT REQUIRED | manter separada da trilha DIO |

## Estado local antes da AWS

Não há bloqueador local conhecido para iniciar a etapa prática do Canvas.

O caminho obrigatório DIO:

- não depende da stack AutoGluon/Lightning;
- possui secret scan;
- possui `DIO submission dependencies` com `pip-audit` sem vulnerabilidades ignoradas;
- possui Actions oficiais pinadas por SHA;
- possui documentação de sanitização, custo e cleanup.

A extensão AutoGluon é opcional e possui audit separado com allowlist restrita ao finding transitivo `PYSEC-2026-3624` enquanto não existir release corrigida compatível. Qualquer finding adicional continua falhando esse job.

## Configuração preparada para a execução

| Campo | Planejamento |
|---|---|
| Tipo | Time Series Forecasting |
| Dataset | `dataset-1000-com-preco-promocional-e-renovacao-estoque.csv` |
| Target | `QUANTIDADE_ESTOQUE` |
| Item ID | `ID_PRODUTO` |
| Timestamp | `DATA_EVENTO` |
| Forecast length | 7 |
| Frequência | diária, conforme detecção/configuração real da interface |
| Colunas adicionais | `PRECO`, `FLAG_PROMOCAO` quando o fluxo real permitir |

A interface real prevalece sobre este planejamento. Registrar o que o Canvas efetivamente disponibilizar.

## Evidências

- matriz: [`14-matriz-evidencias-dio.md`](14-matriz-evidencias-dio.md)
- template de resultados reais: [`15-resultados-canvas.md`](15-resultados-canvas.md)
- kit de screenshots: [`../assets/screenshots/README.md`](../assets/screenshots/README.md)
- guia de execução: [`04-configuracao-sagemaker-canvas.md`](04-configuracao-sagemaker-canvas.md)
- custos: [`10-custos-aws.md`](10-custos-aws.md)
- cleanup: [`12-cleanup-aws.md`](12-cleanup-aws.md)

## Gate automatizado

Execute:

```bash
python scripts/check_dio_submission.py
```

Enquanto Canvas estiver pendente, a saída correta é informativa:

```text
DIO SUBMISSION READY: NO
```

Depois de adicionar todas as evidências reais, use o gate estrito:

```bash
python scripts/check_dio_submission.py --strict
```

O workflow `.github/workflows/dio-readiness.yml` executa a checagem em modo informativo para não deixar o CI vermelho enquanto a pendência é explicitamente a execução AWS.

## Checklist pré-envio

- [ ] upload/import Canvas real concluído;
- [ ] configuração Canvas real registrada;
- [ ] build concluído;
- [ ] métricas reais documentadas;
- [ ] Column impact/características reais documentadas;
- [ ] decisão sobre re-treino documentada;
- [ ] forecast real gerado;
- [ ] export real concluído;
- [ ] conclusões baseadas no Canvas escritas;
- [ ] 9 screenshots reais adicionados e sanitizados;
- [ ] nenhum dado sensível em imagens/commits;
- [ ] logout e cleanup revisados;
- [ ] Billing/Cost Management revisado;
- [ ] todos os checks do head final verdes;
- [ ] `python scripts/check_dio_submission.py --strict` retorna sucesso;
- [ ] PR final revisado;
- [ ] somente então enviar a URL na DIO.

## Decisão atual

**DIO SUBMISSION READY: NO**

**Motivo:** a execução real do SageMaker Canvas e suas evidências ainda não existem. Todo o restante é preparação local para que essa seja a única pendência funcional.
