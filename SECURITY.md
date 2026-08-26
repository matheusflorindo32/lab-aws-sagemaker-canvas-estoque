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

## Varredura automatizada

O script `scripts/scan_secrets.py` procura padrões de alto risco em arquivos de texto, incluindo formatos de AWS Access Key ID, cabeçalhos de private key e atribuições explícitas de credenciais AWS.

O workflow `.github/workflows/security.yml` executa essa varredura em `push`, `pull_request` e execução manual, com permissão mínima `contents: read`.

A varredura automatizada reduz risco, mas não substitui revisão humana nem os mecanismos nativos de proteção/secret scanning que possam estar habilitados no GitHub.

## Screenshots

Antes de versionar qualquer captura de tela da AWS, revise e remova informações desnecessárias como Account ID, e-mail, nomes de usuários IAM, ARNs sensíveis, billing pessoal, chaves, tokens ou outros identificadores privados.

O checklist de evidências está em `assets/screenshots/README.md`.

## Relato de vulnerabilidade

Se encontrar um segredo exposto, não o reproduza em issue pública. Revogue/rotacione a credencial afetada na AWS e remova o segredo do histórico conforme a orientação oficial do provedor.

## Princípio de menor privilégio

Ao executar o Lab, utilize apenas as permissões necessárias para SageMaker Canvas e serviços diretamente relacionados. Evite credenciais de administrador para atividades rotineiras.
