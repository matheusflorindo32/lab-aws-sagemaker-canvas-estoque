# Changelog

## Unreleased

### Added
- Estrutura profissional de documentação para o desafio DIO.
- Baseline de segurança para evitar exposição de credenciais AWS.
- Scanner de segredos em Python com workflow dedicado de segurança.
- Script de validação do dataset sem dependências externas.
- Testes unitários para validação, EDA e scanner de segredos.
- Análise exploratória descritiva reproduzível com resultados verificados em CI.
- Workflow de CI para compilar scripts, executar testes, validar o dataset e rodar a EDA.
- Guia de execução no Amazon SageMaker Canvas.
- Guia de interpretação de métricas de forecasting.
- Checklist de evidências/sanitização de screenshots AWS.
- Documentação de custos e cleanup AWS.
- Política de integridade dos resultados.
- Guia de contribuição.

### Changed
- README reestruturado para apresentar o Lab como case de portfólio, preservando o objetivo original de previsão de estoque.
- Validação do dataset ampliada para cardinalidade, preço negativo, chave `SKU + data`, regularidade temporal e domínio dos campos.
- `.gitignore` ajustado para restringir padrões AWS sem ignorar genericamente qualquer arquivo `config`.
- README atualizado com estatísticas verificadas, status real de CI e separação entre implementado, pendente, experimental e evolução futura.
