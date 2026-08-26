# Inventory Forecasting Studio

## Objetivo

O `app.py` transforma a trilha Python em uma interface visual inspirada em um estúdio AutoML, sem tentar reproduzir ou se passar pelo Amazon SageMaker Canvas.

## Fluxo da aplicação

```text
Dataset
  ↓
Validação e EDA
  ↓
Configuração do horizonte
  ↓
Benchmarks temporais
  ↓
Leaderboard
  ↓
Forecast por SKU
  ↓
P10 / P50 / P90
  ↓
Download CSV
```

Uma aba separada apresenta a integração AutoGluon e só exibe resultados versionados se os arquivos reais existirem em `results/autogluon/`.

## Executar localmente

Crie um ambiente virtual e instale as dependências da aplicação:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements-app.txt
streamlit run app.py
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements-app.txt
streamlit run app.py
```

## Recursos

- visão geral da arquitetura;
- catálogo de modelos;
- preview do dataset;
- EDA por SKU;
- configuração de horizonte;
- execução de benchmarks;
- leaderboard com MAE, RMSE, WAPE, MAPE, MASE e WQL;
- seleção de modelo e SKU;
- gráfico de forecast;
- P10/P50/P90;
- download de leaderboard e forecast;
- status explícito dos artefatos AutoGluon.

## Integridade

A aplicação não preenche resultados ausentes. Se os benchmarks não forem executados na sessão, mostra `não executado`. Se AutoGluon não tiver artefatos reais, a aba correspondente permanece sem leaderboard e orienta a execução do treinamento.

## Deploy opcional

O Streamlit Community Cloud pode executar aplicações diretamente a partir de um repositório GitHub. Para deploy, mantenha as dependências em arquivo de requirements e use a mesma versão de Python validada no ambiente de desenvolvimento.
