# Limitações e Evoluções

## Limitações atuais

Este Lab é intencionalmente educacional e possui limitações que impedem extrapolar seus resultados para uma operação real sem validação adicional:

- série temporal curta;
- apenas 25 SKUs;
- dados educacionais/sintéticos;
- ausência de vendas/demanda explícita;
- ausência de lead time e fornecedor;
- ausência de estoque de segurança e nível de serviço;
- ausência de custos de ruptura e armazenagem;
- ausência de variáveis externas mais ricas;
- forecasting de estoque não equivale diretamente a forecasting de demanda.

## Evoluções de curto prazo

- executar o modelo real no SageMaker Canvas;
- registrar métricas e feature impact;
- exportar forecasts por SKU;
- comparar comportamento promocional vs. não promocional;
- documentar incerteza da previsão quando disponível.

## Evoluções de médio/longo prazo

- modelar demanda/vendas;
- integrar lead time, safety stock e reorder point;
- adicionar sazonalidade, feriados e campanhas;
- armazenar dados em Amazon S3;
- implementar pipeline de ingestão/transformação;
- disponibilizar insights via dashboard ou API;
- monitorar drift e automatizar retraining quando justificável.

Essas evoluções são propostas futuras e não devem ser descritas como já implementadas.
