from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "prototype"


class PublicSnapshotTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(
            (DATA_DIRECTORY / "generation_manifest.json").read_text(encoding="utf-8")
        )
        cls.transfers = pd.read_csv(DATA_DIRECTORY / "transfers.csv")
        cls.fees = pd.read_csv(DATA_DIRECTORY / "fees.csv")
        cls.settlements = pd.read_csv(DATA_DIRECTORY / "settlements.csv")

    def test_snapshot_is_explicitly_synthetic(self) -> None:
        self.assertTrue(self.manifest["synthetic_data"])

    def test_transfer_scale_and_keys(self) -> None:
        self.assertEqual(len(self.transfers), 10_000)
        self.assertTrue(self.transfers["transfer_id"].is_unique)
        self.assertFalse(self.transfers["transfer_id"].isna().any())

    def test_completed_transfer_relationships(self) -> None:
        completed_ids = set(
            self.transfers.loc[
                self.transfers["transfer_status"] == "completed", "transfer_id"
            ]
        )
        self.assertSetEqual(completed_ids, set(self.fees["transfer_id"]))
        self.assertSetEqual(completed_ids, set(self.settlements["transfer_id"]))

    def test_fee_equation(self) -> None:
        expected = self.fees["list_fee_usd"] - self.fees["approved_price_investment_usd"]
        leakage = self.fees["expected_fee_usd"] - self.fees["collected_fee_usd"]
        self.assertTrue(((expected - self.fees["expected_fee_usd"]).abs() <= 0.02).all())
        self.assertTrue(((leakage - self.fees["fee_leakage_usd"]).abs() <= 0.02).all())


if __name__ == "__main__":
    unittest.main()
