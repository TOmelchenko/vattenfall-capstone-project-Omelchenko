# Expected Final Outputs

This document lists all expected outputs at final project submission.

---

## Bronze Tables

Stored in `vattenfall_dev.raw`

| Table | Description |
|---|---|
| `bronze_market_prices` | Raw energy market prices by region and market type |
| `bronze_weather` | Raw weather observations by region |
| `bronze_grid_events` | Raw grid incidents and outages by asset and region |
| `bronze_asset_reference` | Asset reference data |
| `bronze_region_reference` | Region reference data with country code and operating zone |
| `bronze_market_reference` | Market type reference data |
| `bronze_event_type_reference` | Grid event type reference data |
| `bronze_weather_alert_reference` | Weather alert level reference data |

All bronze tables are ingested via Auto Loader or direct read from Unity Catalog volumes. No transformations applied.

---

## Silver Tables

Stored in `vattenfall_dev.refined`

| Table | Description |
|---|---|
| `silver_market_prices` | Cleaned and standardized market prices with `is_high_price` and `price_band` flags |
| `silver_weather` | Cleaned weather data with `is_severe_weather` and `wind_class` classification |
| `silver_grid_events` | Cleaned grid events with `is_critical_event` and `duration_band` classification |
| `silver_integrated` | Grid events enriched with daily market and weather context and reference data |

Silver tables are validated after ingestion. Invalid rows, nulls on key columns, and out-of-range values are removed.

---

## Gold Tables and Views

Stored in `vattenfall_dev.analytics`

| Object | Type | Description |
|---|---|---|
| `gold_regional_operations` | Table | One row per event_date/region - aggregated grid, market, and weather metrics with operational risk classification |
| `gold_market_volatility` | Table | One row per event_date/region - price volatility, price range, and volatility band |
| `vw_operational_dashboard` | View | Dashboard-ready view combining operational risk, weather impact, and event counts |

---

## Validation Evidence

Each layer has a dedicated validation notebook that produces a structured summary DataFrame.

| Notebook | Checks |
|---|---|
| `05_bronze_validation` | Source file presence, table existence, row counts, schema, key field nulls |
| `05_silver_validation` | Table existence, row counts, schema, key field nulls, negative value checks |
| `02_gold_validation` | Row counts, null checks, negative checks, distribution checks, cross-table consistency, taskValues check |

Validation notebooks raise a `ValueError` and stop the pipeline if any check fails.

---

## Dashboard-Ready Structures

| Object | Purpose |
|---|---|
| `vw_operational_dashboard` | Primary dashboard view - combines grid summary and weather impact per region per day |
| `gold_regional_operations` | Operational risk monitor - shows critical event counts, weather impact score, and risk rating |
| `gold_market_volatility` | Market intelligence - shows price volatility, price range, and volatility band per region per day |

---

## Tests

| File | Type | What it checks |
|---|---|---|
| `test_config_presence.py` | pytest | `dev.yml` exists and contains all required keys including gold table names |
| `test_repo_structure.py` | pytest | All expected folders and notebook files exist in the repo |
| `test_transform_contracts.py` | Databricks notebook | Silver transformation functions return expected columns and filter invalid rows correctly |

