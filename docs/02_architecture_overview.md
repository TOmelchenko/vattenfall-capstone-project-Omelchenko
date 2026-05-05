# 02 - Architecture Overview

---

## Platform

This project is built on **Databricks** using the **medallion architecture** - a layered data design pattern that separates raw data from cleaned data from business-ready outputs.

Unity Catalog governs all catalog, schema, table, and volume objects.
Configuration is centralized in `config/dev.yml` and loaded into every notebook via `%run ./00_config`.

---

## Data Domains

The lakehouse combines four source domains:

- **Energy market prices** - spot prices and volume by region and market type
- **Weather observations** - temperature, wind, precipitation, and alert levels by region
- **Grid events** - incidents, outages, and severity by asset and region
- **Reference data** - assets, regions, market types, and weather alert classifications

---

## Medallion Layers

```
Raw CSV Files (Unity Catalog Volumes)
            |
            v
        [ Bronze ]
        Raw ingestion via Auto Loader
        No transformations
        Source of truth for what arrived
            |
            v
        [ Silver ]
        Cleaned, standardized, enriched
        Quality checks applied
        Trusted layer for analysis
            |
            v
        [ Gold ]
        Aggregated, business-ready outputs
        One row per region per day
        Ready to query or visualize
```

---

## Unity Catalog Structure

```
vattenfall_dev/
├── raw/                          - Bronze layer
│   ├── volumes/
│   │   ├── landing/              - Raw CSV files
│   │   └── checkpoints/          - Auto Loader checkpoints
│   └── tables/
│       ├── bronze_market_prices
│       ├── bronze_weather
│       ├── bronze_grid_events
│       ├── bronze_asset_reference
│       ├── bronze_region_reference
│       ├── bronze_market_reference
│       ├── bronze_event_type_reference
│       └── bronze_weather_alert_reference
├── refined/                      - Silver layer
│   └── tables/
│       ├── silver_market_prices
│       ├── silver_weather
│       ├── silver_grid_events
│       └── silver_integrated
└── analytics/                    - Gold layer
    └── tables and views/
        ├── gold_regional_operations
        ├── gold_market_volatility
        └── vw_operational_dashboard
```

---

## Pipeline Sequence

```
Setup UC objects    
    01_setup_uc_objects
        |    
Bronze ingestion (parallel)
  01_market_prices_autoloader
  02_weather_autoloader
  03_grid_events_autoloader
  04_reference_data_load
        |
  05_bronze_validation
        |
Silver transformations (parallel)
  01_market_prices_silver
  02_weather_silver
  03_grid_events_silver
        |
  04_integrated_operational_silver
        |
  05_silver_validation
        |
Gold outputs
  01_gold_outputs
        |
  02_gold_validation
```

---

## Reusable Python Modules

```
src/
├── transforms/       - Silver cleaning and standardization functions
├── udfs/             - PySpark UDFs for classification
└── utils/
    └── validation_utils.py  - Shared validation logic across all layers
```
