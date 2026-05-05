# 01 - Business Context

## Company

Vattenfall is a European energy company operating across electricity generation, distribution, and trading.
Energy operations depend on real-time and historical data from multiple domains to make decisions about pricing, grid stability, and risk.

---

## Business Problem

Operational data arrives from separate systems - market feeds, weather stations, and grid monitoring tools.
Without a unified platform, it is difficult to answer questions like:

- Which regions are at the highest operational risk today?
- How does weather affect energy market prices?
- Which grid events are driving the most disruption?

Data sitting in separate files or systems cannot answer these questions reliably or quickly.

---

## Project Goal

Build a governed data lakehouse on Databricks that combines four operational domains:

- **Energy market prices** - spot prices and volume across market types and regions
- **Weather observations** - temperature, wind speed, precipitation, and alert levels by region
- **Grid events** - incidents, outages, and severity data by asset and region
- **Reference data** - assets, regions, market types, and weather alert classifications

The output is a set of clean, trusted, business-ready gold tables that the operations team can query directly.

---

## Business Value

The gold layer answers three operational questions:

**1. Where is the operational risk highest?**
`gold_regional_operations` shows critical event counts, severe weather flags, and operational risk rating per region per day.

**2. How volatile is the energy market?**
`gold_market_volatility` shows price volatility, price range, and volume across regions and days.

**3. What does the operations dashboard show?**
`vw_operational_dashboard` combines grid events and weather into a single view ready for dashboard consumption.

---

## Scope

This project covers the full data engineering pipeline from raw file landing to gold analytical outputs.
It does not cover machine learning, real-time streaming beyond Auto Loader ingestion, or downstream BI tool integration.
