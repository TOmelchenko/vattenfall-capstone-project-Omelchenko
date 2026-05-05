# 00 - How to Use This Repo

This guide covers everything you need to get started with the project.

---

## 1. Clone the repo into Databricks

1. Open your Databricks workspace
2. Go to **Repos** in the left sidebar
3. Click **Add repo**
4. Paste the GitHub repo URL and click **Create repo**

The repo will appear under `/Workspace/Repos/your-email/vattenfall-capstone-project-Omelchenko`.

---

## 2. Set up configuration

All project settings live in `config/dev.yml`. This file controls catalog names, schema names, volume paths, table names, and business rules.

Open `config/dev.yml` and confirm the catalog name matches your Databricks workspace:

```yaml
catalog: vattenfall_dev
```

No other changes are needed for a standard setup.

---

## 3. Set up the Unity Catalog objects

The notebook `notebooks/01_setup/01_setup_uc_objects` now is part of the job and doesn't require manual run.

---

## 4. Run the pipeline notebooks

The pipeline runs in the following order. Each notebook depends on the previous one completing successfully.

```
notebooks/01_setup/01_setup_uc_objects
                |
                V 
notebooks/02_bronze/01_market_prices_autoloader
notebooks/02_bronze/02_weather_autoloader
notebooks/02_bronze/03_grid_events_autoloader
notebooks/02_bronze/04_reference_data_load
notebooks/02_bronze/05_bronze_validation
                |
                V
notebooks/03_silver/01_market_prices_silver
notebooks/03_silver/02_weather_silver
notebooks/03_silver/03_grid_events_silver
notebooks/03_silver/04_integrated_operational_silver
notebooks/03_silver/05_silver_validation
                |
                V
notebooks/04_gold/01_gold_outputs
notebooks/04_gold/02_gold_validation

```

You can run each notebook manually by opening it and clicking **Run All**, or trigger them all via the Databricks Job (see section 6).

---

## 5. Run the tests

Test notebooks live in `tests/`. Run them manually after the pipeline completes:

```
tests/test_config_presence.py       - checks dev.yml has all required keys
tests/test_repo_structure.py        - checks all expected folders and files exist
tests/test_transform_contracts.py   - checks silver transformation functions return expected columns
```

---

## 6. Trigger the job

The full pipeline is defined in `databricks.yml` as a Databricks Asset Bundle job.

Run the `Vattenfall Energy Operations Pipeline` job manually or trigger the job via `databricks.yml`
```python
%sh
databricks bundle deploy
databricks bundle run vattenfall_pipeline
```
For learning purpouses the job is scheduled to run once per day (schedule currently disabled)

---

## 7. Key files

| File | Purpose |
|---|---|
| `config/dev.yml` | All project settings |
| `notebooks/01_setup/00_config` | Loads config and exposes variables to notebooks |
| `src/utils/validation_utils.py` | Reusable validation functions |
| `src/transforms/` | Silver transformation functions |
| `src/udfs/` | PySpark UDFs |
| `databricks.yml` | Job definition |
