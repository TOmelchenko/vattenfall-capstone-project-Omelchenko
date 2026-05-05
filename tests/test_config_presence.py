"""
test_config_presence.py
Checks that dev.yml exists and contains all required keys.
Run with: pytest tests/test_config_presence.py
"""

import yaml
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "config", "dev.yml"
)

REQUIRED_TOP_LEVEL_KEYS = [
    "catalog",
    "schemas",
    "volumes",
    "landing_paths",
    "checkpoint_paths",
    "bronze_tables",
    "silver_tables",
    "gold_tables",
    "rules",
]

REQUIRED_SCHEMA_KEYS  = ["raw", "refined", "analytics"]
REQUIRED_VOLUME_KEYS  = ["landing", "checkpoints", "raw"]
REQUIRED_BRONZE_KEYS  = ["market_prices", "weather", "grid_events", "asset_reference"]
REQUIRED_SILVER_KEYS  = ["market_prices", "weather", "grid_events", "integrated"]
REQUIRED_GOLD_KEYS    = ["regional_operations", "market_volatility", "dashboard_view"]
REQUIRED_RULE_KEYS    = ["market_prices", "weather", "grid_events"]

REQUIRED_MARKET_PRICE_RULE_KEYS = [
    "min_price_eur_mwh",
    "max_price_eur_mwh",
    "min_volume_mwh",
    "high_price_threshold"
]


def load_config():
    assert os.path.exists(CONFIG_PATH), f"Config file not found: {CONFIG_PATH}"
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def test_config_file_exists():
    assert os.path.exists(CONFIG_PATH), f"dev.yml not found at {CONFIG_PATH}"


def test_top_level_keys_present():
    config = load_config()
    for key in REQUIRED_TOP_LEVEL_KEYS:
        assert key in config, f"Missing top-level key: '{key}'"


def test_catalog_is_string():
    config = load_config()
    assert isinstance(config["catalog"], str), "catalog must be a string"
    assert len(config["catalog"]) > 0, "catalog must not be empty"


def test_schema_keys_present():
    config = load_config()
    for key in REQUIRED_SCHEMA_KEYS:
        assert key in config["schemas"], f"Missing schema key: '{key}'"


def test_volume_keys_present():
    config = load_config()
    for key in REQUIRED_VOLUME_KEYS:
        assert key in config["volumes"], f"Missing volume key: '{key}'"


def test_bronze_table_keys_present():
    config = load_config()
    for key in REQUIRED_BRONZE_KEYS:
        assert key in config["bronze_tables"], f"Missing bronze_tables key: '{key}'"


def test_silver_table_keys_present():
    config = load_config()
    for key in REQUIRED_SILVER_KEYS:
        assert key in config["silver_tables"], f"Missing silver_tables key: '{key}'"


def test_gold_table_keys_present():
    config = load_config()
    for key in REQUIRED_GOLD_KEYS:
        assert key in config["gold_tables"], f"Missing gold_tables key: '{key}'"


def test_gold_table_values_are_strings():
    config = load_config()
    for key, value in config["gold_tables"].items():
        assert isinstance(value, str), f"gold_tables.{key} must be a string"
        assert len(value) > 0, f"gold_tables.{key} must not be empty"


def test_rules_keys_present():
    config = load_config()
    for key in REQUIRED_RULE_KEYS:
        assert key in config["rules"], f"Missing rules key: '{key}'"


def test_market_price_rules_have_thresholds():
    config = load_config()
    mp_rules = config["rules"]["market_prices"]
    for key in REQUIRED_MARKET_PRICE_RULE_KEYS:
        assert key in mp_rules, f"Missing market_prices rule: '{key}'"


def test_gold_regional_operations_value():
    config = load_config()
    assert config["gold_tables"]["regional_operations"] == "gold_regional_operations", \
        "gold_tables.regional_operations must be 'gold_regional_operations'"


def test_gold_market_volatility_value():
    config = load_config()
    assert config["gold_tables"]["market_volatility"] == "gold_market_volatility", \
        "gold_tables.market_volatility must be 'gold_market_volatility'"


def test_gold_dashboard_view_value():
    config = load_config()
    assert config["gold_tables"]["dashboard_view"] == "vw_operational_dashboard", \
        "gold_tables.dashboard_view must be 'vw_operational_dashboard'"