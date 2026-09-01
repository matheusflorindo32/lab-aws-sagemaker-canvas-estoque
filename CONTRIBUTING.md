# Contributing

Este projeto evolui um Lab educacional da DIO preservando rastreabilidade com a fonte original.

## Fluxo recomendado

1. Crie uma branch a partir de `main`.
2. Faça alterações pequenas e focadas.
3. Execute as verificações locais antes do PR:

```bash
python -m py_compile scripts/*.py
python -m unittest discover -s tests -v
python scripts/validate_dataset.py
python scripts/analyze_dataset.py
python scripts/scan_secrets.py
```

4. Revise se nenhum segredo AWS ou dado sensível foi incluído.
5. Abra um Pull Request descrevendo objetivo, arquivos alterados, testes e pendências.

## Padrão de commits

Use Conventional Commits quando possível:

- `feat:` nova funcionalidade;
- `docs:` documentação;
- `test:` testes;
- `fix:` correção;
- `security:` segurança;
- `ci:` automação;
- `chore:` manutenção.

## Dados

Não sobrescreva silenciosamente os datasets originais da DIO. Dados derivados devem indicar origem e transformação.

## Resultados experimentais

Não adicione métricas, forecasts, screenshots ou conclusões de modelo como resultados reais sem evidência da execução no SageMaker Canvas.

## Segurança

Nunca publique credenciais AWS. Consulte `SECURITY.md` antes de adicionar prints, arquivos de configuração ou automações.
