# Inventory Forecasting Studio

## Objetivo

O `app.py` transforma a trilha Python em uma interface visual de análise de forecasting. Ele **não reproduz nem se apresenta como Amazon SageMaker Canvas**.

## Fluxo atual

```text
Dataset
  ↓
Validação / EDA
  ↓
Holdout interativo + rolling-origin oficial
  ↓
Benchmarks
  ↓
AutoGluon TimeSeries
  ↓
Seleção interna × desempenho externo
  ↓
P10 / P50 / P90 + calibração
  ↓
Diagnóstico por horizonte e SKU
  ↓
Forecast / exports
```

## O que a interface mostra

### Visão geral

- arquitetura executada;
- catálogo de modelos;
- distinção explícita entre trilha Python e Canvas não executado.

### Dados & EDA

- preview do dataset;
- preço médio;
- estoque médio;
- percentual promocional;
- série temporal por SKU.

### Benchmarks

O usuário pode executar um holdout interativo. A interface também informa que a validação oficial do repositório utiliza três folds rolling-origin/expanding-window com testes externos não sobrepostos.

### AutoGluon

Se `results/validated/` estiver disponível, a aba mostra:

- WAPE médio dos três folds;
- WQL médio;
- coverage P10–P90;
- vitórias externas do WeightedEnsemble;
- tabela de estabilidade;
- calibração por horizonte;
- diagnóstico agregado por SKU;
- leaderboard do holdout final.

A interface diferencia:

- **selection stability** — estabilidade da escolha pela validação interna;
- **external test stability** — estabilidade do desempenho nos testes externos.

No experimento P1 atual, a seleção interna foi estável, mas a estabilidade externa foi classificada como `unstable`.

### Forecast

- seleção de modelo/SKU para os benchmarks interativos;
- P10/P50/P90;
- valor real do holdout;
- download CSV;
- aviso de que quantis produzidos não implicam calibração perfeita.

---

## Executar localmente

```bash
python -m venv .venv
```

### Linux/macOS

```bash
source .venv/bin/activate
pip install -r requirements-app.txt
streamlit run app.py
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements-app.txt
streamlit run app.py
```

## Reproduzir AutoGluon P1

```bash
pip install -r requirements-ml.txt
python scripts/train_autogluon.py --time-limit 180 --presets medium_quality
python scripts/train_autogluon_multifold.py --time-limit 180 --presets medium_quality
```

## Integridade

A aplicação não fabrica resultados ausentes. Arquivos de evidência validados ficam em `results/validated/`; artifacts completos de execução continuam disponíveis no GitHub Actions pelo período de retenção configurado.

O Studio é classificado como **demonstrador funcional / projeto de portfólio**, não como produto production-ready. Não possui autenticação, banco transacional, jobs persistentes, model serving ou política automática de reposição.

## Próximo nível de produto

Uma evolução futura deve priorizar decisão operacional, não adicionar mais frameworks:

`demanda/vendas + estoque atual + lead time → forecast → safety stock → reorder point → recomendação`

Essa arquitetura futura não está implementada nesta versão.
