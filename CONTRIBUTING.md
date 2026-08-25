# Contributing

Este projeto evolui um Lab educacional da DIO preservando rastreabilidade com a fonte original.

## Fluxo recomendado

1. Crie uma branch a partir de `main`.
2. Faça alterações pequenas e focadas.
3. Execute `python scripts/validate_dataset.py` ao alterar dados ou validações.
4. Revise se nenhum segredo AWS ou dado sensível foi incluído.
5. Abra um Pull Request descrevendo objetivo, arquivos alterados e evidências de validação.

## Padrão de commits

Use Conventional Commits quando possível:

- `feat:` nova funcionalidade;
- `docs:` documentação;
- `fix:` correção;
- `security:` segurança;
- `ci:` automação;
- `chore:` manutenção.

## Dados

Não sobrescreva silenciosamente os datasets originais da DIO. Dados derivados devem indicar origem e transformação.

## Segurança

Nunca publique credenciais AWS. Consulte `SECURITY.md` antes de adicionar prints, arquivos de configuração ou automações.
