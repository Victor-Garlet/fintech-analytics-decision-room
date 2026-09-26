PYTHON := .venv/bin/python
DBT := .venv/bin/dbt

.PHONY: setup test test-internal load dbt-build dbt-docs export readme-visuals build regenerate clean

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests -p "test_public*.py" -v

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

readme-visuals: dbt-build
	$(PYTHON) scripts/build_readme_visuals.py

build: test dbt-docs export readme-visuals

regenerate:
	$(PYTHON) scripts/generate_prototype.py

clean:
	cd dbt_fintech && ../$(DBT) clean --profiles-dir .
