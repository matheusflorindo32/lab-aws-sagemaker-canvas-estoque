# Security Policy

## Escopo

Este repositório contém duas trilhas separadas:

1. **trilha obrigatória de submissão DIO / SageMaker Canvas**;
2. **extensão opcional de portfólio com Python, Streamlit e AutoGluon TimeSeries**.

Nenhuma credencial AWS deve ser armazenada, publicada ou incluída em screenshots, exemplos, workflows ou arquivos de configuração.

## Estado de segurança da submissão DIO

A submissão DIO **não depende da stack AutoGluon/Lightning** para executar o fluxo exigido pelo desafio no SageMaker Canvas.

O gate obrigatório `DIO submission dependencies` executa `pip-audit` em `requirements-app.txt` **sem ignorar vulnerabilidades**. O secret scanner também é obrigatório.

Isso significa que a vulnerabilidade transitiva de Lightning descrita abaixo **não faz parte do caminho obrigatório usado para a submissão DIO**.

## Extensão opcional AutoGluon

`requirements-ml.txt` pertence à extensão experimental/portfólio. Ela não é necessária para:

- importar o dataset no Canvas;
- configurar target/item ID/timestamp;
- treinar no SageMaker Canvas;
- analisar métricas/feature importance do Canvas;
- gerar e exportar previsões do Canvas;
- enviar o repositório na plataforma DIO.

A stack ML opcional continua auditada separadamente pelo job `Optional AutoGluon dependency advisory`, sem suprimir findings do scanner.

## Finding conhecido — CVE-2026-58659 / PYSEC-2026-3624

Em 30/08/2026, a release PyPI `lightning 2.6.5` continua afetada por `CVE-2026-58659 / PYSEC-2026-3624`. A correção existe no código upstream, mas ainda não há release PyPI corrigida disponível nesta data.

O advisory descreve execução arbitrária de código quando um checkpoint malicioso controla o campo `_instantiator` e é carregado por `LightningModule.load_from_checkpoint`.

No projeto atual:

- não há upload de checkpoints por usuários;
- não há endpoint para carregar checkpoints externos;
- o fluxo DIO não importa Lightning;
- a dependência aparece somente na extensão opcional AutoGluon.

Portanto, o risco **não é declarado como corrigido upstream**. Ele é **isolado do caminho obrigatório de submissão DIO** e permanece visível no audit da extensão opcional.

### Regra até existir release corrigida

- não carregar checkpoints arbitrários/não confiáveis;
- não transformar a extensão AutoGluon em serviço público que aceite modelos/checkpoints externos;
- manter o audit da stack opcional ativo;
- remover esta seção quando uma versão corrigida compatível for publicada e validada pelo CI.

## Segredos que nunca devem ser versionados

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- arquivos `.env`
- diretórios `.aws/`
- chaves `*.pem`, `*.key`, `*.p12`, `*.pfx`

## Varredura automatizada

O script `scripts/scan_secrets.py` procura padrões de alto risco em arquivos de texto, incluindo formatos de AWS Access Key ID, cabeçalhos de private key e atribuições explícitas de credenciais AWS.

O workflow `.github/workflows/security.yml` executa:

- secret-pattern scanning;
- audit obrigatório das dependências necessárias ao caminho de submissão;
- audit separado da extensão AutoGluon.

Os workflows usam `contents: read` e GitHub Actions oficiais pinadas por commit SHA.

## Screenshots AWS

Antes de versionar qualquer captura de tela da AWS, remova ou oculte:

- Account ID;
- e-mail;
- username IAM;
- ARNs sensíveis;
- billing pessoal;
- access keys;
- session tokens;
- URLs assinadas;
- qualquer outro identificador privado desnecessário.

O checklist de evidências está em `assets/screenshots/README.md`.

## Relato de vulnerabilidade

Se encontrar um segredo exposto, não o reproduza em issue pública. Revogue/rotacione a credencial afetada na AWS e remova o segredo do histórico conforme a orientação oficial do provedor.

## Princípio de menor privilégio

Ao executar o Lab, utilize apenas as permissões necessárias para SageMaker Canvas e serviços diretamente relacionados. Evite credenciais de administrador para atividades rotineiras.
