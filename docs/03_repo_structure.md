# 03 - Repository Structure

This project uses a layered repository structure. Each layer has a single responsibility, making the codebase easier to navigate, reuse, and maintain.

---

## Structure

```
vattenfall-capstone-project-Omelchenko/
├── config/
│   └── dev.yml                       - All project settings and business rules
├── docs/
│   ├── 00_how_to_use_this_repo.md
│   ├── 01_business_context.md
│   ├── 02_architecture_overview.md
│   └── 03_repo_structure.md
├── notebooks/
│   ├── 01_setup/
│   │   ├── 00_config                 - Shared config loader for all notebooks
│   │   └── 01_setup_uc_objects       - One-time Unity Catalog setup
│   ├── 02_bronze/
│   │   ├── 01_market_prices_autoloader
│   │   ├── 02_weather_autoloader
│   │   ├── 03_grid_events_autoloader
│   │   ├── 04_reference_data_load
│   │   └── 05_bronze_validation
│   ├── 03_silver/
│   │   ├── 01_market_prices_silver
│   │   ├── 02_weather_silver
│   │   ├── 03_grid_events_silver
│   │   ├── 04_integrated_operational_silver
│   │   └── 05_silver_validation
│   ├── 04_gold/
│   │   ├── 01_gold_outputs
│   │   └── 02_gold_validation
│   └── 05_governance/
│       └── 01_governance
├── sample_data/
│   ├── market_prices/
│   ├── weather/
│   ├── grid_events/
│   └── reference/
├── src/
│   ├── transforms/
│   │   ├── market_prices_cleaning.py
│   │   ├── weather_cleaning.py
│   │   ├── grid_events_cleaning.py
│   │   └── business_rules.py
│   ├── udfs/
│   │   ├── market_prices_udfs.py
│   │   ├── weather_udfs.py
│   │   └── grid_events_udfs.py
│   └── utils/
│       └── validation_utils.py
├── tests/
│   ├── test_config_presence.py
│   ├── test_repo_structure.py
│   └── test_transform_contracts.py
├── .github/workflows/                - Repository automation checks
├── databricks.yml                    - Databricks Asset Bundle job definition
└── README.md
```

---

## Layer Descriptions

**`config/`**
Single source of truth for all project settings - catalog name, schema names, volume paths, table names, and business rules. No values are hardcoded in notebooks.

**`docs/`**
Project documentation covering business context, architecture, repo structure, and usage guide.

**`notebooks/`**
Databricks workflow notebooks organized by pipeline stage. Each notebook does one thing and depends on `00_config` for shared variables.

**`sample_data/`**
Raw CSV files organized by domain. Files are copied into Unity Catalog volumes during the bronze ingestion step.

**`src/`**
Reusable Python modules imported into notebooks. Split into three subfolders - transforms for cleaning logic, udfs for PySpark user-defined functions, and utils for shared validation logic.

**`tests/`**
Validation scripts that run independently of the pipeline. Two files run locally with pytest, one runs as a Databricks notebook.

**`.github/workflows/`**
GitHub Actions automation that runs repository checks on every push.

**`databricks.yml`**
Defines the full pipeline as a Databricks Asset Bundle job with task dependencies.

---

## Design Principle

A strong engineering repository makes responsibilities visible. When someone opens this repo for the first time, they should immediately understand what each folder does and where to find what they need.
