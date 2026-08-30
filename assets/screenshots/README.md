# Evidências reais do SageMaker Canvas

> Esta pasta deve conter **somente screenshots reais e sanitizados** da execução AWS. Não criar imagens fictícias, mocks ou placeholders `.png` para satisfazer o checklist.

## Kit obrigatório/recomendado

| Arquivo | O que deve provar | O que evitar/excluir |
|---|---|---|
| `01-canvas-home.png` | contexto de que a atividade foi realizada no SageMaker Canvas | Account ID, e-mail, IAM username, dados administrativos |
| `02-import-dataset.png` | seleção/upload/import do CSV usado no Lab | caminhos locais pessoais, buckets/ARNs sensíveis, URLs assinadas |
| `03-dataset-preview.png` | dataset importado e schema/colunas reconhecidos | identificadores administrativos desnecessários |
| `04-model-configuration.png` | tipo Time Series Forecasting, target, item ID, timestamp e forecast length reais | inventar configuração diferente da UI real |
| `05-training.png` | build iniciado/concluído e modelo real | dados sensíveis da conta |
| `06-model-analysis.png` | métricas reais exibidas na página Analyze | números da trilha Python sobrepostos ou adicionados manualmente |
| `07-feature-importance.png` | Column impact / características que influenciam a previsão | interpretação causal não suportada |
| `08-forecast.png` | previsão real gerada pelo modelo Canvas | forecast produzido pelo AutoGluon apresentado como Canvas |
| `09-export.png` | ação/resultado de export real | URL assinada, token, credencial ou bucket privado desnecessário |

## Sanitização antes do commit

Ocultar/remover sempre que aparecer:

- AWS Account ID;
- endereço de e-mail;
- IAM username/role quando não for necessário à evidência;
- Access Key ID, Secret Access Key ou Session Token;
- ARNs sensíveis;
- URLs assinadas;
- informações pessoais de Billing/Cost Management;
- nomes de recursos privados que não agreguem valor ao Lab.

## Regra de autenticidade

- não editar números/métricas da interface;
- não montar screenshots compostos que alterem o significado da tela;
- recorte e blur de dados sensíveis são permitidos;
- manter informação suficiente para o avaliador reconhecer a etapa;
- se uma tela mudou na interface atual do Canvas, documentar o que a interface realmente mostrou em vez de tentar reproduzir uma tela antiga.

## Status atual

Nenhum `.png` real foi adicionado porque o SageMaker Canvas ainda não foi executado nesta trilha. Isso é intencional e evita evidência falsa.
