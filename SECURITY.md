# Security Policy

## Scope

Este repositório é um projeto educacional de Machine Learning com Amazon SageMaker Canvas. Nenhuma credencial AWS deve ser armazenada, publicada ou incluída em screenshots, exemplos, workflows ou arquivos de configuração.

## Segredos que nunca devem ser versionados

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- arquivos `.env`
- diretórios `.aws/`
- chaves `*.pem`, `*.key`, `*.p12`, `*.pfx`

## Screenshots

Antes de versionar qualquer captura de tela da AWS, revise e remova informações desnecessárias como Account ID, e-mail, nomes de usuários IAM, ARNs sensíveis, billing pessoal, chaves, tokens ou outros identificadores privados.

## Relato de vulnerabilidade

Se encontrar um segredo exposto, não o reproduza em issue pública. Revogue/rotacione a credencial afetada na AWS e remova o segredo do histórico conforme a orientação oficial do provedor.

## Princípio de menor privilégio

Ao executar o Lab, utilize apenas as permissões necessárias para SageMaker Canvas e serviços diretamente relacionados. Evite credenciais de administrador para atividades rotineiras.
