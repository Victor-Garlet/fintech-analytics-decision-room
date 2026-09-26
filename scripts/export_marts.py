from __future__ import annotations

import json
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "warehouse" / "fintech_analytics.duckdb"
EXPORT_DIRECTORY = PROJECT_ROOT / "data" / "exports"

MARTS = [
    "mart_executive_kpis",
    "mart_corridor_performance",
    "mart_provider_performance",
    "mart_take_rate_bridge",
    "mart_reporting_period_reconciliation",
    "mart_speed_cost_tradeoff",
    "mart_routing_scenario",
    "mart_fee_leakage_hotspots",
    "mart_reconciliation_exceptions",
    "mart_transfer_unit_economics",
]


def sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def main() -> int:
    if not WAREHOUSE_PATH.exists():
        raise SystemExit("Warehouse not found. Run `make dbt-build` first.")

    EXPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "synthetic_data": True,
        "source_schema": "marts",
        "tables": {},
    }

    with duckdb.connect(str(WAREHOUSE_PATH), read_only=True) as connection:
        for mart in MARTS:
            output_path = EXPORT_DIRECTORY / f"{mart}.parquet"
            connection.execute(
                f"copy marts.{mart} to '{sql_path(output_path)}' "
                "(format parquet, compression zstd)"
            )
            row_count = connection.execute(
                f"select count(*) from marts.{mart}"
            ).fetchone()[0]
            manifest["tables"][mart] = {
                "rows": row_count,
                "file": output_path.name,
            }
            print(f"{mart}: {row_count:,} rows")

    manifest_path = EXPORT_DIRECTORY / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
