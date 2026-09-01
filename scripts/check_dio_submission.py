from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SCREENSHOTS = (
    "01-canvas-home.png",
    "02-import-dataset.png",
    "03-dataset-preview.png",
    "04-model-configuration.png",
    "05-training.png",
    "06-model-analysis.png",
    "07-feature-importance.png",
    "08-forecast.png",
    "09-export.png",
)

REQUIRED_FILES = (
    "README.md",
    "datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv",
    "docs/13-checklist-submissao-dio.md",
    "docs/15-resultados-canvas.md",
)


@dataclass(frozen=True)
class ReadinessReport:
    ready: bool
    missing: list[str]


def check_readiness(root: Path) -> ReadinessReport:
    root = Path(root)
    missing: list[str] = []

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            missing.append(relative)

    checklist = root / "docs/13-checklist-submissao-dio.md"
    if checklist.is_file():
        text = checklist.read_text(encoding="utf-8")
        if "DIO SUBMISSION READY: YES" not in text:
            missing.append("docs/13-checklist-submissao-dio.md does not declare DIO SUBMISSION READY: YES")

    results = root / "docs/15-resultados-canvas.md"
    if results.is_file():
        text = results.read_text(encoding="utf-8")
        if "PENDING REAL EXECUTION" in text:
            missing.append("docs/15-resultados-canvas.md still contains PENDING REAL EXECUTION")

    screenshots_dir = root / "assets/screenshots"
    for name in REQUIRED_SCREENSHOTS:
        path = screenshots_dir / name
        if not path.is_file() or path.stat().st_size == 0:
            missing.append(f"assets/screenshots/{name}")

    return ReadinessReport(ready=not missing, missing=missing)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether local DIO Canvas submission evidence is complete.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory).")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 when evidence is incomplete. Without --strict, readiness is informational.",
    )
    args = parser.parse_args()

    report = check_readiness(args.root)
    print(f"DIO SUBMISSION READY: {'YES' if report.ready else 'NO'}")
    if report.missing:
        print("Missing:")
        for item in report.missing:
            print(f"- {item}")

    if args.strict and not report.ready:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
