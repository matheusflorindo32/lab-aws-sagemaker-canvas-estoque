# Guia ultra-didático — Amazon SageMaker Canvas

> **STATUS: PENDING REAL EXECUTION**
>
> **AWS EXECUTION AUTHORIZED = NO**
>
> Este guia prepara a execução prática do desafio DIO sem iniciar recursos faturáveis e sem inventar resultados. Antes de clicar em qualquer build/prediction, consulte [`10-custos-aws.md`](10-custos-aws.md) e obtenha autorização explícita.

## O que a DIO exige

O Lab oficial pede: selecionar/upload do dataset, importar no Canvas, configurar entradas/saída, treinar, analisar métricas e características relevantes, prever, exportar e documentar conclusões.

## Dataset

Use exatamente:

```text
datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv
```

Configuração planejada:

| Campo | Valor planejado |
|---|---|
| Problem type | Time series forecasting |
| Target column | `QUANTIDADE_ESTOQUE` |
| Item ID column | `ID_PRODUTO` |
| Time stamp column | `DATA_EVENTO` |
| Forecast length | `7` |
| Frequência | diária, conforme detecção/configuração atual do Canvas |
| Colunas adicionais | `PRECO`, `FLAG_PROMOCAO` quando reconhecidas/permitidas no fluxo real |
| Objective metric | registrar a escolha real; Canvas pode escolher uma default |

> A interface atual prevalece sobre os nomes planejados acima. Se um rótulo ou opção tiver mudado, registre o que a AWS realmente mostrar.

---

# Antes de abrir o Canvas

1. Confirme a conta e a região AWS que serão usadas.
2. Confirme elegibilidade de Free Tier, se houver.
3. Defina um teto financeiro autorizado antes de qualquer build.
4. Deixe o CSV pronto no computador.
5. Abra [`../assets/screenshots/README.md`](../assets/screenshots/README.md) para saber quais evidências coletar.
6. Não use credenciais de administrador quando não forem necessárias.
7. Não publique Account ID, e-mail, IAM username, ARN sensível, access keys, tokens, billing ou URLs assinadas.

---

# Passo 1 — Entrar na AWS

1. Entre na AWS Management Console com a conta destinada ao Lab.
2. Confirme a região.
3. Não registre em screenshots identificadores administrativos desnecessários.

Evidência recomendada depois de abrir o Canvas:

`assets/screenshots/01-canvas-home.png`

---

# Passo 2 — Abrir o SageMaker Canvas

1. Abra Amazon SageMaker.
2. Entre na aplicação SageMaker Canvas disponível para sua conta/domínio.
3. Aguarde o workspace carregar.

> A cobrança de workspace termina quando a sessão/aplicação é encerrada conforme a AWS; fechar apenas a aba não é o procedimento de cleanup.

---

# Passo 3 — Importar o dataset

1. No Canvas, vá para a área de datasets/importação.
2. Escolha a opção de import/local upload compatível com a interface atual.
3. Selecione:

```text
dataset-1000-com-preco-promocional-e-renovacao-estoque.csv
```

4. Confirme a importação.
5. Confira se aparecem as cinco colunas esperadas:
   - `ID_PRODUTO`
   - `DATA_EVENTO`
   - `PRECO`
   - `FLAG_PROMOCAO`
   - `QUANTIDADE_ESTOQUE`
6. Confira os tipos inferidos, principalmente `DATA_EVENTO` como data/hora compatível.

Evidências:

- `02-import-dataset.png`
- `03-dataset-preview.png`

---

# Passo 4 — Criar o modelo

Na documentação atual da AWS para time series:

1. Abra **My models**.
2. Escolha **New model**.
3. Dê um nome simples e não sensível ao modelo.
4. Selecione **Time series forecasting**.
5. Selecione o dataset importado.
6. No **Build** tab, escolha a coluna target.

Target planejado:

```text
QUANTIDADE_ESTOQUE
```

---

# Passo 5 — Configure model

Abra **Configure model** e registre a configuração real.

Planejamento:

```text
Item ID column = ID_PRODUTO
Time stamp column = DATA_EVENTO
Forecast length = 7
```

A AWS informa atualmente que o Forecast length usa a unidade temporal detectada nos dados.

Se houver opções adicionais:

- `Group column`: não adicionar sem necessidade do Lab;
- holiday schedule: opcional, não necessário para este dataset educacional;
- Objective metric: registrar a métrica realmente escolhida/default;
- Algorithms: aparecem no Standard build; não selecionar modelos extras apenas por aparência.

Evidência:

`04-model-configuration.png`

---

# Passo 6 — Escolher Quick Build ou Standard Build

A documentação atual informa que time-series forecasting suporta os dois modos:

## Quick Build

- tempo médio publicado: aproximadamente **2–20 minutos**;
- usa um único algoritmo tree-based;
- menor tempo operacional para uma primeira execução.

## Standard Build

- tempo médio publicado: aproximadamente **2–4 horas**;
- permite seleção de algoritmos;
- Canvas treina múltiplos candidatos e pode construir ensemble;
- custo/tempo potencialmente maiores.

## Decisão recomendada para o Lab

Não iniciar nenhuma opção antes da autorização financeira.

Depois de autorizado, **começar pela menor execução que satisfaça a evidência DIO**. Quick Build é a primeira opção a considerar para reduzir tempo/custo; Standard Build só deve ser escolhido se a interface/evidência necessária ou o objetivo pedagógico justificar o custo adicional.

Não assumir que Standard é obrigatório: o README da DIO exige treinamento/análise, não um tipo específico de build.

---

# Passo 7 — Treinar

1. Revise novamente dataset/configuração.
2. Verifique a estimativa/avisos de custo exibidos pela conta, se disponíveis.
3. Somente com autorização explícita, inicie o build escolhido.
4. Espere o modelo chegar ao estado pronto para análise.

Evidência:

`05-training.png`

---

# Passo 8 — Analisar métricas

Na página **Analyze** de modelos time-series, a AWS documenta atualmente métricas como:

- Average Weighted Quantile Loss (Average wQL);
- WAPE;
- RMSE;
- MAPE;
- MASE.

Registre **somente as métricas efetivamente apresentadas na sua execução** em:

`docs/15-resultados-canvas.md`

Evidência:

`06-model-analysis.png`

Não copiar métricas AutoGluon para esta seção.

---

# Passo 9 — Column impact / características relevantes

A documentação atual da AWS informa que a página Analyze de time series possui **Column impact**, que representa o peso relativo de cada coluna nas previsões.

1. Registre as colunas realmente mostradas.
2. Registre scores/percentuais somente se visíveis.
3. Não interprete Column impact como causalidade.
4. Se a interface não mostrar esse bloco na execução específica, documente a ausência em vez de inventar resultado.

Evidência:

`07-feature-importance.png`

---

# Passo 10 — Decidir se re-treino é necessário

O README da DIO diz para fazer ajustes e re-treinar **se necessário**.

Depois do primeiro build, documente uma decisão objetiva em `docs/15-resultados-canvas.md`:

- `Re-treino necessário: NÃO` + justificativa; ou
- `Re-treino necessário: SIM` + o que será alterado e por quê.

Não executar segundo treino apenas para marcar checklist.

---

# Passo 11 — Gerar previsão

Use o modelo treinado para gerar uma previsão real de estoque conforme as opções da interface.

Registre:

- SKU(s) escolhido(s), se aplicável;
- horizonte mostrado;
- P10/P50/P90 se exibidos;
- observações relevantes sem superinterpretar.

Evidência:

`08-forecast.png`

---

# Passo 12 — Exportar

1. Use o mecanismo de export/download disponível na interface atual.
2. Salve o export real somente se não contiver dados sensíveis.
3. Quando apropriado, coloque o arquivo em `results/exports/`.
4. Registre nome/tipo do export em `docs/15-resultados-canvas.md`.

Evidência:

`09-export.png`

---

# Passo 13 — Conclusões

Preencha `docs/15-resultados-canvas.md` com:

- configuração real;
- build type;
- métricas;
- Column impact;
- previsão;
- export;
- decisão sobre re-treino;
- insights;
- limitações;
- custo/cleanup verificáveis.

Depois atualize o README, sem misturar resultados Python e Canvas.

---

# Passo 14 — Verificação automática

Antes de enviar à DIO:

```bash
python scripts/check_dio_submission.py --strict
```

O resultado esperado somente após todas as evidências reais é:

```text
DIO SUBMISSION READY: YES
```

Se retornar `NO`, não enviar ainda.

---

# Passo 15 — Logout e cleanup

Ao terminar, siga integralmente:

[`12-cleanup-aws.md`](12-cleanup-aws.md)

A etapa não termina no screenshot/export: precisa incluir logout/revisão de recursos e Billing.

---

## Referências oficiais consultadas em 30/08/2026

- Build a model — SageMaker Canvas: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-build-model-how-to.html
- How custom models work: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-build-model.html
- Metrics reference: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-metrics.html
- Evaluate model performance: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-scoring.html
- Advanced model settings: https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-advanced-settings.html
- Canvas pricing: https://aws.amazon.com/sagemaker/ai/canvas/pricing/
