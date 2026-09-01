# Resultados do Modelo

Este diretório receberá apenas resultados reais exportados do Amazon SageMaker Canvas.

## Organização sugerida

- `predictions/` — previsões por SKU ou lote;
- `metrics/` — tabelas/resumos de métricas;
- `exports/` — arquivos temporários exportados da interface.

## Regra de integridade

Nenhum valor deve ser apresentado como resultado experimental antes da execução real do modelo. Enquanto a etapa AWS estiver pendente, o README principal e a documentação devem utilizar explicitamente `PENDENTE`.

## Após o treinamento

Registrar:

1. data da execução;
2. configuração do modelo;
3. horizonte de previsão;
4. métricas realmente exibidas;
5. SKUs analisados;
6. arquivos exportados;
7. interpretação técnica;
8. interpretação de negócio;
9. limitações observadas.
