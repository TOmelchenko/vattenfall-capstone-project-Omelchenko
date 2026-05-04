# 03 - Repository Structure

This project uses a layered repository structure. Each layer has a single responsibility, making the codebase easier to navigate, reuse, and maintain.

---

## Structure

```
vattenfall-capstone-project-Omelchenko/
├── docs/                        # Project documentation
├── config/                      # Project settings and configuration
├── sample_data/                 # Raw source data organized by domain
├── sql/                         # Reusable SQL logic
├── src/                         # Reusable Python logic
├── notebooks/                   # Databricks workflow notebooks
├── tests/                       # Validation and quality checks
└── .github/workflows/           # Repository automation checks
```

---

## Layer Descriptions

**`docs/`**
Contains all project documentation - architecture overview, business context, and usage guides. Written for both technical and non-technical readers.

**`config/`**
Stores project settings such as catalog names, schema names, volume paths, and business rules. Centralizing configuration here means notebooks and scripts never hardcode values.

**`sample_data/`**
Organizes raw source files by domain - energy market prices, weather observations, grid telemetry, and reference data. Files land here before being ingested into the lakehouse.

**`sql/`**
Stores reusable SQL - transformation logic, views, and merge statements. Keeping SQL in files rather than inline strings makes it easier to version, test, and review.

**`src/`**
Contains reusable Python modules shared across notebooks - helper functions, schema definitions, and utility logic. Notebooks import from here instead of duplicating code.

**`notebooks/`**
Contains the Databricks workflow notebooks that make up the pipeline - one notebook per stage. These are the job tasks that run in sequence.

**`tests/`**
Prepares validation logic - data quality checks, schema assertions, and row count comparisons. Separating tests from pipeline notebooks keeps the workflow clean.

**`.github/workflows/`**
Stores GitHub Actions automation - repository checks that run on every push, such as file structure validation or linting.

---

## Design Principle

A strong engineering repository makes responsibilities visible. When someone opens this repo for the first time, they should immediately understand what each folder does and where to find what they need.
