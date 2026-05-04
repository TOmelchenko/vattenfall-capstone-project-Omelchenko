# 02 - Architecture Overview

> This document will be expanded once the full pipeline design is confirmed.

---

## Platform

This project is built on **Databricks** using the **medallion architecture** - a layered data design pattern that separates raw data from cleaned data from business-ready outputs.

---

## Data Domains

The lakehouse combines four source domains:

- **Energy market prices** - spot prices and market signals
- **Weather observations** - temperature, wind, and conditions by region
- **Grid telemetry and incident events** - operational grid data and outage records
- **Reference data** - locations, assets, and lookup tables

---

## Medallion Layers

```
Raw Files (Volumes)
      |
      v
  [ Bronze ]  - raw ingestion, no transformations
      |
      v
  [ Silver ]  - cleaned, validated, enriched
      |
      v
  [ Gold ]    - aggregated, business-ready outputs
```

**Bronze** - data lands as-is from the source. No changes. The source of truth for what arrived.

**Silver** - data is cleaned, standardized, and enriched. Quality checks run here. This is the trusted layer.

**Gold** - data is aggregated into business-facing reports. Simple, fast, and ready to query.

---

## Governance

Unity Catalog manages all catalog, schema, table, and volume objects. Configuration is stored in `config/project_config.yml` and shared across notebooks via `%run ./00_config`.

---
## TODO
> Sections to be added: pipeline diagram, job task sequence, data flow per domain.
