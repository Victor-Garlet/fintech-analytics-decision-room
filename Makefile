PYTHON := .venv/bin/python
DBT := .venv/bin/dbt

.PHONY: setup test test-internal load dbt-build dbt-docs export build regenerate clean

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests -p "test_public_snapshot.py" -v

test-internal:
	$(PYTHON) -m unittest discover -s tests -v

load:
	$(PYTHON) scripts/load_duckdb.py

dbt-build: load
	cd dbt_fintech && ../$(DBT) build --profiles-dir .

dbt-docs: dbt-build
	cd dbt_fintech && ../$(DBT) docs generate --profiles-dir .

export: dbt-build
	$(PYTHON) scripts/export_marts.py

build: test dbt-docs

regenerate:
	$(PYTHON) scripts/generate_prototype.py

clean:
	cd dbt_fintech && ../$(DBT) clean --profiles-dir .
