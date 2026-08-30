# Custos AWS no Lab

> Verificação de preços: **30/08/2026**. Os valores abaixo vêm da página oficial de pricing do Amazon SageMaker Canvas e são referências em USD; cobrança real depende da região, recursos efetivamente usados e condições da conta.

O Amazon SageMaker Canvas segue modelo **pay-as-you-go**. A cobrança pode envolver workspace, processamento, treinamento e previsão.

## Gate FinOps para este projeto

**AUTORIZAÇÃO AWS NECESSÁRIA: SIM**

Nenhum treinamento, previsão ou outro recurso potencialmente faturável deve ser iniciado sem autorização explícita após revisão da tela de preço/estimativa da conta usada no Lab.

## Workspace Canvas

A documentação oficial de pricing informa cobrança de **US$ 1,90 por hora de sessão** do workspace após eventual franquia aplicável. O tempo começa quando o Canvas é iniciado e termina quando o usuário faz logout ou o administrador encerra a aplicação. Fechar apenas a aba do navegador não deve ser tratado como confirmação de encerramento.

A AWS informa também um **Free Tier de 2 meses**, com até **160 horas/mês de workspace Canvas**. A elegibilidade depende da conta e deve ser confirmada antes da execução; o Free Tier de workspace não significa treinamento gratuito.

## Processamento do dataset

O dataset deste Lab é muito menor que 5 GB. A tabela atual de pricing do Canvas informa **US$ 0** para importação/amostragem de datasets abaixo de 5 GB no fluxo padrão do workspace. Transformações ou recursos adicionais podem alterar a cobrança.

## Treinamento de modelo tabular/time series

Para datasets pequenos, Canvas utiliza instâncias SageMaker Training e cobra pelas horas de treinamento. Na tabela oficial atual, um **Standard build** com dataset **<100 MB** aparece com estimativa de **US$ 2,30 a US$ 9,20** para treinamento.

Esse intervalo é uma referência de pricing da AWS, **não uma previsão de que esta execução custará exatamente isso**. Canvas seleciona os recursos de treino automaticamente e o valor real depende da execução/região.

### Quick build vs Standard build

A documentação oficial do Canvas informa que modelos de time series aceitam ambos:

- **Quick build**: execução mais curta e uso de um único algoritmo tree-based;
- **Standard build**: exploração de múltiplos algoritmos e ensemble, normalmente com maior tempo e custo potencial.

A documentação indica tempos médios aproximados de:

- Quick build time series: **2–20 minutos**;
- Standard build time series: **2–4 horas**.

Para uma primeira evidência do desafio, a escolha deve considerar o que a DIO realmente exige e o custo mostrado pela conta antes do clique de treinamento. Não escolher Standard build apenas por aparência de sofisticação.

## Previsões de séries temporais

Para time series, a AWS informa cobrança específica de inferência:

- **single prediction**: SageMaker Asynchronous Inference, com mínimo de 2 horas; faixa publicada de aproximadamente **US$ 0,408–0,533/h** dependendo da região, encerrando após duas horas ociosas;
- **batch prediction de 0–5 GB**: estimativa publicada de aproximadamente **US$ 1,25–2,03**.

Por isso, gerar previsão também exige revisão do custo antes da execução.

## Cenários de custo para o Lab

Os valores abaixo são apenas limites de planejamento baseados nas tabelas oficiais, não faturas previstas:

| Componente | Referência oficial atual | Como tratar no Lab |
|---|---:|---|
| Workspace | US$ 1,90/h | minimizar tempo e fazer logout ao terminar |
| Import/amostragem <5 GB | US$ 0 | dataset atual é muito pequeno |
| Standard build <100 MB | US$ 2,30–9,20 | confirmar estimativa/região antes de executar |
| Single time-series prediction | US$ 0,408–0,533/h, mínimo 2 h | evitar se não for necessário para evidência |
| Batch prediction 0–5 GB | US$ 1,25–2,03 | usar somente se realmente exigido |

## Estratégia de menor custo

1. Confirmar elegibilidade do Free Tier da conta.
2. Entrar no Canvas apenas quando o dataset e checklist já estiverem preparados.
3. Importar somente o CSV principal validado.
4. Preferir a menor execução que cumpra a evidência DIO; comparar Quick vs Standard antes do build.
5. Não criar endpoint em tempo real.
6. Gerar apenas as previsões necessárias para demonstrar o fluxo.
7. Capturar screenshots sanitizados imediatamente após a execução.
8. Exportar as evidências necessárias.
9. Fazer logout do Canvas.
10. Executar o cleanup em [`12-cleanup-aws.md`](12-cleanup-aws.md) e revisar Billing/Cost Explorer.

## Teto operacional recomendado

Este repositório **não define automaticamente um teto financeiro em nome do usuário**. Antes da execução real, deve-se registrar um teto autorizado com base na moeda/limite desejado e interromper o fluxo se a estimativa apresentada pela AWS superar esse teto.

## Registro de custo real

**PENDENTE — preencher apenas após execução autorizada e com informação verificável do Billing da conta usada no Lab.**

Não publicar Account ID, e-mail, IAM username, ARN sensível, billing ID ou outros dados administrativos para comprovar custo.

## Fontes oficiais

- Amazon SageMaker Canvas Pricing: https://aws.amazon.com/sagemaker/ai/canvas/pricing/
- Build a model — SageMaker Canvas: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-build-model-how-to.html
- SageMaker pricing: https://aws.amazon.com/sagemaker/ai/pricing/
