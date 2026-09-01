import io
import unittest

from src.inventory_forecasting.data import load_dataset_file


class DataUploadTests(unittest.TestCase):
    def test_load_dataset_file_accepts_uploaded_csv_bytes(self) -> None:
        payload = io.BytesIO(
            b"ID_PRODUTO,DATA_EVENTO,PRECO,FLAG_PROMOCAO,QUANTIDADE_ESTOQUE\n"
            b"A,2024-01-01,10.5,0,100\n"
            b"A,2024-01-02,11.0,1,95\n"
        )

        rows = load_dataset_file(payload)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["ID_PRODUTO"], "A")
        self.assertEqual(rows[1]["PRECO"], 11.0)
        self.assertEqual(rows[1]["FLAG_PROMOCAO"], 1)
        self.assertEqual(rows[1]["QUANTIDADE_ESTOQUE"], 95.0)


if __name__ == "__main__":
    unittest.main()
