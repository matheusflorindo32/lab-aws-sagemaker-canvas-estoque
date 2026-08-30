import tempfile
import unittest
from pathlib import Path

from scripts.check_dio_submission import check_readiness


class DioReadinessTests(unittest.TestCase):
    def _base_tree(self, root: Path) -> None:
        (root / "datasets").mkdir(parents=True)
        (root / "docs").mkdir(parents=True)
        (root / "assets" / "screenshots").mkdir(parents=True)
        (root / "README.md").write_text("# DIO\n", encoding="utf-8")
        (root / "datasets" / "dataset-1000-com-preco-promocional-e-renovacao-estoque.csv").write_text(
            "ID_PRODUTO,DATA_EVENTO,PRECO,FLAG_PROMOCAO,QUANTIDADE_ESTOQUE\n",
            encoding="utf-8",
        )
        (root / "docs" / "13-checklist-submissao-dio.md").write_text("DIO SUBMISSION READY: NO\n", encoding="utf-8")
        (root / "docs" / "15-resultados-canvas.md").write_text("STATUS: PENDING REAL EXECUTION\n", encoding="utf-8")

    def test_reports_pending_canvas_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._base_tree(root)

            report = check_readiness(root)

            self.assertFalse(report.ready)
            self.assertIn("docs/15-resultados-canvas.md still contains PENDING REAL EXECUTION", report.missing)
            self.assertIn("assets/screenshots/01-canvas-home.png", report.missing)

    def test_reports_ready_when_all_required_evidence_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._base_tree(root)
            (root / "docs" / "13-checklist-submissao-dio.md").write_text("DIO SUBMISSION READY: YES\n", encoding="utf-8")
            (root / "docs" / "15-resultados-canvas.md").write_text("STATUS: EXECUTED\nReal Canvas results recorded.\n", encoding="utf-8")
            for name in (
                "01-canvas-home.png",
                "02-import-dataset.png",
                "03-dataset-preview.png",
                "04-model-configuration.png",
                "05-training.png",
                "06-model-analysis.png",
                "07-feature-importance.png",
                "08-forecast.png",
                "09-export.png",
            ):
                (root / "assets" / "screenshots" / name).write_bytes(b"real-evidence-placeholder-for-test")

            report = check_readiness(root)

            self.assertTrue(report.ready)
            self.assertEqual(report.missing, [])


if __name__ == "__main__":
    unittest.main()
