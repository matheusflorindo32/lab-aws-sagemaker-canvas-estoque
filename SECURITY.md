# Security Policy

## Scope

Este repositório é um projeto educacional de Machine Learning com Amazon SageMaker Canvas e uma trilha open source em Python. Nenhuma credencial AWS deve ser armazenada, publicada ou incluída em screenshots, exemplos, workflows ou arquivos de configuração.

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
- `pip-audit` sobre as dependências do Streamlit;
- `pip-audit` sobre as dependências de Machine Learning.

Os workflows usam `contents: read` e GitHub Actions oficiais pinadas por commit SHA.

A varredura automatizada reduz risco, mas não substitui revisão humana nem os mecanismos nativos de proteção/secret scanning que possam estar habilitados no GitHub.

## Exceção temporária conhecida — PYSEC-2026-3624 / CVE-2026-58659

Em 30/08/2026, `pip-audit` detectou `PYSEC-2026-3624` em `lightning 2.6.5`, resolvido transitivamente pela stack de Machine Learning. O advisory descreve execução arbitrária de código quando um checkpoint malicioso controla o campo `_instantiator` e é carregado por `LightningModule.load_from_checkpoint`.

Situação verificada nesta data:

- o advisory afeta Lightning até 2.6.5;
- a correção existe no código upstream, mas ainda não há release PyPI corrigida indicada pelo scanner;
- o preset `medium_quality` deste projeto usa modelos estatísticos/tabulares e modelos pré-treinados Chronos-2/Toto-2;
- este repositório não oferece upload de checkpoint e não chama `LightningModule.load_from_checkpoint` com conteúdo fornecido pelo usuário.

Por isso, enquanto não existir release corrigida compatível, o CI pode ignorar **somente** `PYSEC-2026-3624` de forma explícita. Isso é uma aceitação temporária de risco por baixa reachability no fluxo atual, não uma declaração de que a dependência é segura.

### Condições da exceção

A exceção deve ser removida imediatamente quando ocorrer qualquer uma destas situações:

1. uma release corrigida compatível de Lightning ficar disponível;
2. o projeto passar a aceitar checkpoints externos ou não confiáveis;
3. algum modelo/pipeline introduzir chamada ao caminho vulnerável;
4. uma nova evidência indicar exploração relevante mesmo sem checkpoint fornecido pelo usuário.

Até lá:

- não carregar checkpoints arbitrários/não confiáveis;
- manter `pip-audit` ativo;
- manter a exceção restrita ao identificador exato;
- reavaliar a cada atualização das dependências de ML.

## Screenshots

Antes de versionar qualquer captura de tela da AWS, revise e remova informações desnecessárias como Account ID, e-mail, nomes de usuários IAM, ARNs sensíveis, billing pessoal, chaves, tokens ou outros identificadores privados.

O checklist de evidências está em `assets/screenshots/README.md`.

## Relato de vulnerabilidade

Se encontrar um segredo exposto, não o reproduza em issue pública. Revogue/rotacione a credencial afetada na AWS e remova o segredo do histórico conforme a orientação oficial do provedor.

## Princípio de menor privilégio

Ao executar o Lab, utilize apenas as permissões necessárias para SageMaker Canvas e serviços diretamente relacionados. Evite credenciais de administrador para atividades rotineiras.
