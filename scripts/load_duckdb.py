from __future__ import annotations

import sys
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIRECTORY = PROJECT_ROOT / "data" / "prototype"
PARQUET_DIRECTORY = PROJECT_ROOT / "data" / "parquet"
WAREHOUSE_PATH = PROJECT_ROOT / "data" / "warehouse" / "fintech_analytics.duckdb"

TABLES = [
    "customers",
    "corridors",
    "providers",
    "pricing_rules",
    "quotes",
    "transfers",
    "fees",
    "provider_costs",
    "settlements",
    "support_contacts",
    "refunds",
]


def sql_path(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def main() -> int:
    missing = [name for name in TABLES if not (DATA_DIRECTORY / f"{name}.csv").exists()]
    if missing:
        print(f"Missing prototype files: {', '.join(missing)}", file=sys.stderr)
        return 1

    WAREHOUSE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PARQUET_DIRECTORY.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(WAREHOUSE_PATH)) as connection:
        connection.execute("create schema if not exists raw")
        for table in TABLES:
            csv_path = sql_path(DATA_DIRECTORY / f"{table}.csv")
            parquet_path = sql_path(PARQUET_DIRECTORY / f"{table}.parquet")
            connection.execute(
                f"""
                create or replace table raw.{table} as
                select * from read_csv_auto('{csv_path}', header = true, sample_size = -1)
                """
            )
            connection.execute(
                f"copy raw.{table} to '{parquet_path}' (format parquet, compression zstd)"
            )

        loaded = connection.execute(
            """
            select table_name, estimated_size
            from duckdb_tables()
            where schema_name = 'raw'
            order by table_name
            """
        ).fetchall()

    print(f"Created {WAREHOUSE_PATH}")
    for table_name, row_count in loaded:
        print(f"raw.{table_name}: {row_count:,} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
