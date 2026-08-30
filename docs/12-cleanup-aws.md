# Cleanup da AWS após o Lab

> Objetivo: encerrar a sessão do SageMaker Canvas, revisar recursos relacionados e reduzir o risco de cobrança inesperada. Não excluir recursos compartilhados ou administrados por terceiros sem confirmar o impacto.

## 1. Antes de encerrar

- [ ] Exporte os resultados realmente necessários.
- [ ] Registre métricas e conclusões em `docs/15-resultados-canvas.md`.
- [ ] Capture os screenshots sanitizados necessários.
- [ ] Confirme que nenhum arquivo local/export contém credencial AWS.

## 2. Encerrar o workspace Canvas

A página oficial de pricing informa que a cobrança de workspace termina quando o usuário faz **logout do SageMaker Canvas** ou quando o administrador encerra a aplicação. Fechar somente a aba do navegador não deve ser tratado como encerramento.

- [ ] Use o mecanismo de logout/encerramento disponível na interface atual do Canvas.
- [ ] Confirme que a aplicação/sessão não permanece ativa no console SageMaker.

## 3. Revisar recursos SageMaker

No console AWS, confira os recursos relacionados ao Lab que a conta permitir visualizar:

- [ ] aplicação/workspace Canvas;
- [ ] modelos/builds criados para o Lab;
- [ ] predictions/jobs ainda em execução;
- [ ] endpoints de inferência — este Lab não deve criar endpoint real-time por padrão;
- [ ] jobs de Batch Transform/Asynchronous Inference, se algum foi criado;
- [ ] recursos de Processing/Data Wrangler relacionados, quando aplicável.

Não apague recursos apenas porque têm nomes parecidos. Confirme propriedade e finalidade primeiro.

## 4. Revisar armazenamento

- [ ] Confira datasets/exports criados especificamente para o Lab.
- [ ] Confira buckets/prefixos S3 somente se o fluxo utilizado os criou.
- [ ] Remova apenas artefatos exclusivamente seus e que não sejam mais necessários.
- [ ] Não exclua bucket compartilhado, bucket gerenciado, domínio ou recurso corporativo/educacional sem autorização.

## 5. Verificar cobrança

- [ ] Abra AWS Billing/Cost Management conforme as permissões da conta.
- [ ] Consulte Cost Explorer/charges quando disponível.
- [ ] Procure por custos SageMaker/Canvas e serviços relacionados usados na sessão.
- [ ] Registre em `docs/15-resultados-canvas.md` apenas uma informação de custo que possa ser comprovada, sem publicar billing ID ou dados pessoais.

> Alguns custos podem levar tempo para aparecer. Ausência imediata de cobrança não deve ser documentada como “custo zero” sem evidência suficiente.

## 6. Segurança pós-execução

Antes de commit/push das evidências:

- [ ] Account ID ocultado;
- [ ] e-mail ocultado;
- [ ] IAM username/role ocultado quando desnecessário;
- [ ] nenhum Access Key ID;
- [ ] nenhum Secret Access Key;
- [ ] nenhum Session Token;
- [ ] ARNs sensíveis ocultados;
- [ ] URLs assinadas removidas;
- [ ] informações de billing pessoais ocultadas.

Execute também:

```bash
python scripts/scan_secrets.py
python scripts/check_dio_submission.py --strict
```

## 7. Critério de cleanup concluído

Marcar cleanup como concluído somente quando:

1. as evidências necessárias já estiverem salvas;
2. logout/encerramento do Canvas tiver sido confirmado;
3. não houver job de previsão/treino deliberadamente deixado em execução;
4. recursos relacionados tiverem sido revisados;
5. Billing/Cost Management tiver sido consultado quando a conta permitir;
6. `docs/15-resultados-canvas.md` registrar a situação real.

## Princípio de segurança

Se a conta for corporativa, educacional ou gerenciada, as políticas do administrador prevalecem. Não alterar domínio SageMaker, IAM, buckets ou recursos compartilhados apenas para “limpar” o Lab.
