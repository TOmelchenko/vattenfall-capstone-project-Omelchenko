# Vattenfall Energy Operations Lakehouse

A Databricks data engineering capstone project that combines energy market prices, weather observations, grid events, and reference data into a governed lakehouse with bronze, silver, and gold layers.

---

## Documentation

- [00 - How to use this repo](docs/00_how_to_use_this_repo.md)
- [01 - Business context](docs/01_business_context.md)
- [02 - Architecture overview](docs/02_architecture_overview.md)
- [03 - Repository structure](docs/03_repo_structure.md)

---

## Quick start

1. Clone the repo into Databricks Repos
2. Confirm `config/dev.yml` matches your workspace catalog name
3. Run the `Vattenfall Energy Operations Pipeline` job manually or trigger the job via `databricks.yml`
```python
%sh
databricks bundle deploy
databricks bundle run vattenfall_pipeline
```
For learning purpouses the job is scheduled to run once per day (schedule currently disabled)
See [00 - How to use this repo](docs/00_how_to_use_this_repo.md) for full setup instructions.

---

## Stack

- Databricks with Unity Catalog
- PySpark and Delta Lake
- Auto Loader for bronze ingestion
- Medallion architecture - bronze, silver, gold
- Databricks Asset Bundles for job orchestration
- pytest for local testing

