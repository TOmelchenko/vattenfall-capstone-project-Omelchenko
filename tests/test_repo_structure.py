"""
test_repo_structure.py
Checks that all expected folders and notebook files exist in the repo.
Run with: pytest tests/test_repo_structure.py
"""

import os

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")

EXPECTED_FOLDERS = [
    "config",
    "docs",
    "notebooks",
    "notebooks/01_setup",
    "notebooks/02_bronze",
    "notebooks/03_silver",
    "notebooks/04_gold",
    "notebooks/05_governance",
    "sample_data",
    "sql",
    "src",
    "tests",
]

EXPECTED_FILES = [
    "config/dev.yml",
    "databricks.yml",
    "README.md",
    "notebooks/01_setup/00_config.ipynb",
    "notebooks/01_setup/01_setup_uc_objects.ipynb",
    "notebooks/02_bronze/01_market_prices_autoloader.ipynb",
    "notebooks/02_bronze/02_weather_autoloader.ipynb",
    "notebooks/02_bronze/03_grid_events_autoloader.ipynb",
    "notebooks/02_bronze/04_reference_data_load.ipynb",
    "notebooks/02_bronze/05_bronze_validation.ipynb",
    "notebooks/03_silver/01_market_prices_silver.ipynb",
    "notebooks/03_silver/02_weather_silver.ipynb",
    "notebooks/03_silver/03_grid_events_silver.ipynb",
    "notebooks/03_silver/04_silver_reference_data.ipynb",
    "notebooks/03_silver/05_integrated_operational_silver.ipynb",
    "notebooks/03_silver/06_silver_validation.ipynb",
    "notebooks/04_gold/01_gold_outputs.ipynb",
    "notebooks/04_gold/02_gold_validation.ipynb",
    "notebooks/05_governance/01_governance.ipynb",
 
]


def test_expected_folders_exist():
    for folder in EXPECTED_FOLDERS:
        path = os.path.join(REPO_ROOT, folder)
        assert os.path.isdir(path), f"Missing folder: {folder}"


def test_expected_files_exist():
    for file in EXPECTED_FILES:
        path = os.path.join(REPO_ROOT, file)
        assert os.path.isfile(path), f"Missing file: {file}"