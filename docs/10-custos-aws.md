# FinOps — custos AWS para o Lab SageMaker Canvas

> Verificação de fontes oficiais: **30/08/2026**. Valores em USD. A cobrança real depende da região, recursos selecionados, duração da sessão e condições da conta.

# Gate

**AWS EXECUTION AUTHORIZED = NO**

Nenhum build, prediction ou outro recurso potencialmente faturável deve ser iniciado até existir autorização explícita e um teto financeiro definido pelo usuário.

---

# 1. Workspace Canvas

A página oficial do SageMaker Canvas informa:

- workspace: **US$ 1,90 por hora de sessão**;
- a contagem começa quando a aplicação Canvas é iniciada;
- termina quando o usuário faz logout do Canvas ou quando o administrador encerra a aplicação;
- fechar somente a aba do navegador não é o procedimento de encerramento.

## Free Tier

A AWS informa atualmente um Free Tier de **2 meses**, incluindo até **160 horas/mês de workspace Canvas**.

Isso precisa ser confirmado para a conta usada no Lab. Free Tier do workspace **não significa que model training/prediction serão gratuitos**.

---

# 2. Processamento de dados

A página oficial informa processamento de até **5 GB** dentro do workspace sem cobrança adicional de data processing no fluxo descrito.

Tabela oficial de import/sample:

| Dataset | Estimativa publicada |
|---|---:|
| <5 GB | US$ 0 |

O dataset do Lab é muito menor que esse limite.

---

# 3. Treinamento

Canvas suporta AutoML para modelos tabulares e time-series e cobra o uso das instâncias SageMaker Training selecionadas pelo serviço.

Para **Standard build**, a tabela oficial atual publica a seguinte estimativa para datasets pequenos:

| Dataset | Estimativa total publicada |
|---|---:|
| <100 MB | **US$ 2,30–9,20** |

Esse intervalo é uma referência da AWS, não uma promessa do custo desta execução.

## Quick Build vs Standard Build

A documentação oficial atual informa para time-series forecasting:

- Quick Build: tempo médio aproximado de **2–20 minutos**;
- Standard Build: tempo médio aproximado de **2–4 horas**.

Quick Build usa um único algoritmo tree-based. Standard Build permite múltiplos algoritmos e ensemble.

A tabela de pricing acima é explicitamente apresentada pela AWS como estimativa de **Standard build**. Não inventar um valor específico para Quick Build se a conta/interface não fornecer estimativa suficiente.

### Estratégia recomendada

Para a primeira execução DIO, avaliar Quick Build primeiro porque o README do desafio exige treinar/analisar/prever, mas não exige Standard Build. Só usar Standard se a evidência/objetivo pedagógico justificar custo e tempo maiores.

---

# 4. Previsões time-series

A página oficial atual informa:

## Single prediction

SageMaker Asynchronous Inference:

- mínimo de **2 horas**;
- aproximadamente **US$ 0,408–0,533/h**, dependendo da região;
- cobrança encerra automaticamente após duas horas ociosas segundo a página de pricing.

## Batch prediction

Para 0–5 GB, a tabela oficial publica estimativa total de aproximadamente:

**US$ 1,25–2,03**

composta por EMR Serverless + SageMaker Batch Transform.

Não gerar prediction adicional apenas para enriquecer portfólio se uma única evidência já cumprir o Lab.

---

# 5. Cenários de planejamento

Estes cenários não são faturas previstas; servem para decisão antes da execução.

## Melhor cenário razoável

- conta elegível ao Free Tier de workspace;
- sessão curta;
- dataset <5 GB;
- Quick Build suficiente;
- apenas a previsão necessária para evidência;
- logout imediatamente após coleta/export.

**Custo exato: NÃO COMPROVADO antes da execução.**

Não assumir “zero” porque treinamento e prediction podem ter cobrança mesmo quando workspace estiver dentro do Free Tier.

## Cenário esperado para controle

- workspace curto;
- dataset pequeno;
- um único build;
- uma única previsão/export;
- sem endpoints real-time;
- sem re-treino se não houver necessidade metodológica.

A referência oficial de Standard Build <100 MB é **US$ 2,30–9,20**, à qual podem se somar workspace fora do Free Tier e custos de prediction.

## Cenário conservador

- conta sem Free Tier aplicável;
- sessão mais longa;
- Standard Build;
- previsão time-series;
- necessidade justificada de re-treino.

Nesse cenário, interromper a execução se a estimativa observável/limite autorizado for ultrapassado.

---

# 6. Teto financeiro

O repositório não escolhe um teto em nome do usuário.

Antes da Fase AWS, registrar:

```text
AUTHORIZED MAXIMUM SPEND: <valor definido pelo usuário>
REGION: <região confirmada>
AWS EXECUTION AUTHORIZED: YES
```

Enquanto isso não existir:

```text
AWS EXECUTION AUTHORIZED = NO
```

---

# 7. Estratégia de menor custo

1. Confirmar elegibilidade ao Free Tier.
2. Confirmar região.
3. Definir teto financeiro.
4. Entrar no Canvas apenas com dataset/checklist preparados.
5. Importar somente o CSV principal.
6. Considerar Quick Build primeiro.
7. Não criar endpoint real-time.
8. Fazer apenas a previsão/export necessários para a DIO.
9. Capturar evidências imediatamente.
10. Fazer logout do Canvas.
11. Executar [`12-cleanup-aws.md`](12-cleanup-aws.md).
12. Revisar Billing/Cost Management.

---

# 8. Registro do custo real

**PENDENTE — preencher somente após execução autorizada.**

O valor real, se observável, deve ser registrado em `docs/15-resultados-canvas.md` sem publicar Account ID, billing ID, e-mail ou outros dados administrativos.

Ausência imediata de cobrança não deve ser descrita como custo final zero sem evidência suficiente, pois dados de billing podem ter atraso.

---

# Fontes oficiais

- SageMaker Canvas pricing: https://aws.amazon.com/sagemaker/ai/canvas/pricing/
- Build a model: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-build-model-how-to.html
- How custom models work: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-build-model.html
- SageMaker pricing: https://aws.amazon.com/sagemaker/ai/pricing/
