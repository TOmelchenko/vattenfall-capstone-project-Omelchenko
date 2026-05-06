# Databricks notebook source

# COMMAND ----------

import sys
import os
import yaml

repo_path = "/Workspace/Repos/adb-tetiana@startsteps.org/vattenfall-capstone-project-Omelchenko"
config_path = f"{repo_path}/config/dev.yml"

sys.path.insert(0, f"{repo_path}/src")

with open(config_path) as f:
    config = yaml.safe_load(f)

rules = config["rules"]

from transforms.market_prices_cleaning import standardize_market_prices_columns, filter_invalid_market_prices_rows
from transforms.weather_cleaning import standardize_weather_columns, filter_invalid_weather_rows
from transforms.grid_events_cleaning import standardize_grid_events_columns, filter_invalid_grid_events_rows
from transforms.business_rules import add_market_prices_flags, add_weather_flags, add_grid_events_flags

print("Imports successful.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Sample DataFrames

# COMMAND ----------

def make_market_prices_df():
    data = [("2026-05-04", "NORTH", "DAY_AHEAD", "52.6", "1200", "MARKET_FEED_A", "2026-05-04 08:00:00", "2026-05-04 08:00:00")]
    schema = "event_date string, region string, market_type string, price_eur_mwh string, volume_mwh string, source_system string, last_updated_ts string, ingestion_ts string"
    return spark.createDataFrame(data, schema=schema)


def make_weather_df():
    data = [("2026-05-04", "NORTH", "11.2", "18.5", "0.2", "LOW", "WEATHER_FEED_A", "2026-05-04 08:00:00")]
    schema = "event_date string, region string, temperature_c string, wind_speed_kmh string, precipitation_mm string, weather_alert_level string, source_system string, last_updated_ts string"
    return spark.createDataFrame(data, schema=schema)


def make_grid_events_df():
    data = [("GE1001", "2026-05-04", "NORTH", "ASSET_001", "OUTAGE", "HIGH", "24", "GRID_FEED_A", "2026-05-04 08:00:00")]
    schema = "event_id string, event_date string, region string, asset_id string, event_type string, severity string, duration_minutes string, source_system string, last_updated_ts string"
    return spark.createDataFrame(data, schema=schema)

print("Sample DataFrames ready.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: market prices - standardize returns expected columns

# COMMAND ----------

df = standardize_market_prices_columns(make_market_prices_df())
expected = {"event_date", "region", "market_type", "price_eur_mwh", "volume_mwh", "source_system", "last_updated_ts", "report_day"}
missing = expected - set(df.columns)
assert not missing, f"FAILED: standardize_market_prices_columns missing columns: {missing}"
print("PASSED: standardize_market_prices_columns returns expected columns.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: market prices - filter removes negative prices

# COMMAND ----------

data = [("2026-05-04", "NORTH", "DAY_AHEAD", "-5.0", "1200", "FEED", "2026-05-04 08:00:00", "2026-05-04 08:00:00")]
schema = "event_date string, region string, market_type string, price_eur_mwh string, volume_mwh string, source_system string, last_updated_ts string, ingestion_ts string"
df = spark.createDataFrame(data, schema=schema)
df = standardize_market_prices_columns(df)
result = filter_invalid_market_prices_rows(df, rules)
assert result.count() == 0, "FAILED: negative price rows should be filtered out."
print("PASSED: filter_invalid_market_prices_rows removes negative prices.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: market prices - flags add is_high_price column

# COMMAND ----------

df = standardize_market_prices_columns(make_market_prices_df())
result = add_market_prices_flags(df, rules)
assert "is_high_price" in result.columns, "FAILED: is_high_price column missing."
print("PASSED: add_market_prices_flags adds is_high_price column.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: weather - standardize returns expected columns

# COMMAND ----------

df = standardize_weather_columns(make_weather_df())
expected = {"event_date", "region", "temperature_c", "wind_speed_kmh", "precipitation_mm", "weather_alert_level"}
missing = expected - set(df.columns)
assert not missing, f"FAILED: standardize_weather_columns missing columns: {missing}"
print("PASSED: standardize_weather_columns returns expected columns.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: weather - flags add is_severe_weather column

# COMMAND ----------

df = standardize_weather_columns(make_weather_df())
result = add_weather_flags(df, rules)
assert "is_severe_weather" in result.columns, "FAILED: is_severe_weather column missing."
print("PASSED: add_weather_flags adds is_severe_weather column.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: grid events - standardize returns expected columns

# COMMAND ----------

df = standardize_grid_events_columns(make_grid_events_df())
expected = {"event_id", "event_date", "region", "asset_id", "event_type", "severity", "duration_minutes"}
missing = expected - set(df.columns)
assert not missing, f"FAILED: standardize_grid_events_columns missing columns: {missing}"
print("PASSED: standardize_grid_events_columns returns expected columns.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: grid events - flags add is_critical_event column

# COMMAND ----------

df = standardize_grid_events_columns(make_grid_events_df())
result = add_grid_events_flags(df, rules)
assert "is_critical_event" in result.columns, "FAILED: is_critical_event column missing."
print("PASSED: add_grid_events_flags adds is_critical_event column.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Test: grid events - filter removes null event_id

# COMMAND ----------

data = [(None, "2026-05-04", "NORTH", "ASSET_001", "OUTAGE", "HIGH", "24", "FEED", "2026-05-04 08:00:00")]
schema = "event_id string, event_date string, region string, asset_id string, event_type string, severity string, duration_minutes string, source_system string, last_updated_ts string"
df = spark.createDataFrame(data, schema=schema)
df = standardize_grid_events_columns(df)
result = filter_invalid_grid_events_rows(df, rules)
assert result.count() == 0, "FAILED: rows with null event_id should be filtered out."
print("PASSED: filter_invalid_grid_events_rows removes null event_id rows.")

# COMMAND ----------

print()
print("=" * 50)
print("ALL TRANSFORM CONTRACT TESTS PASSED")
print("=" * 50)