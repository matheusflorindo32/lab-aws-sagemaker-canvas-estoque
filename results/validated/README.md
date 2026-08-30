# Resultados validados P1/P2

Este diretório preserva resultados pequenos e auditáveis obtidos de execuções reais do GitHub Actions. Não contém modelos, checkpoints ou caches.

## Proveniência

### AutoGluon
- workflow run: `33339001646`
- artifact: `inventory-forecasting-autogluon` (`9739968837`)
- artifact digest: `sha256:32ac52fe9d069861563720073fde4b3c3c615bade20dd8f9cd30b453b9356a5f`
- code head executado: `ebe2cae5dfe3d94e4df9433e121bf082403289c6`
- dataset SHA-256: `fe8ffe48cc34cd8540ecba10984066fe503b0bb5ca9d55f9280d5b1960649031`
- AutoGluon TimeSeries: `1.6.1`
- seed: `123`
- protocolo: 3 folds rolling-origin/expanding-window, testes externos não sobrepostos de 7 dias, treinos de 19/26/33 pontos por SKU.

### Benchmarks
- workflow run: `33334277877`
- artifact: `inventory-forecasting-benchmarks` (`9738542182`)
- artifact digest: `sha256:f5edf5e58447a532cc12bebecbd5f7b9ddbbc28bfe655d3158a8ac92de02624f`

## Interpretação importante

`WeightedEnsemble` foi selecionado pela validação interna do AutoGluon nos 3 folds, mas venceu o teste externo em 2/3. No fold 1, `Chronos2` teve WQL menor e o ensemble ficou em 3º. Por isso, `selection_stability=stable` e `external_test_stability=unstable` são conceitos distintos.

O coverage médio P10–P90 foi 0,672381, abaixo dos 0,80 nominais. Os quantis são reais, mas não estão perfeitamente calibrados neste dataset curto.

Os arquivos desta pasta são evidência de um experimento educacional e não de desempenho em produção.