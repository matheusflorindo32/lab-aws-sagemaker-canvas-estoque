from __future__ import annotations

import argparse
from pathlib import Path

from src.inventory_forecasting.autogluon_runner import run_autogluon_backtest


def main() -> None:
    parser = argparse.ArgumentParser(description="Treina e avalia AutoGluon TimeSeries no holdout temporal de 7 dias.")
    parser.add_argument("--time-limit", type=int, default=300, help="Limite de treino em segundos.")
    parser.add_argument("--presets", default="medium_quality", help="Preset do AutoGluon TimeSeries.")
    args = parser.parse_args()

    result = run_autogluon_backtest(time_limit=args.time_limit, presets=args.presets)
    output_dir = Path("results/autogluon")
    output_dir.mkdir(parents=True, exist_ok=True)

    result["leaderboard"].to_csv(output_dir / "leaderboard.csv", index=False)
    result["predictions"].reset_index().to_csv(output_dir / "holdout_predictions.csv", index=False)
    result["feature_importance"].to_csv(output_dir / "feature_importance.csv")

    evaluation = result["evaluation"]
    with (output_dir / "evaluation.txt").open("w", encoding="utf-8") as handle:
        for key, value in evaluation.items():
            handle.write(f"{key}={value}\n")

    print("=== AutoGluon TimeSeries ===")
    print(f"Configuração: {result['config']}")
    print("Avaliação real do holdout:")
    for key, value in evaluation.items():
        print(f"{key}={value}")
    print(f"Artefatos exportados em: {output_dir}")


if __name__ == "__main__":
    main()
