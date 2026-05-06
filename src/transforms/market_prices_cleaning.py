from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def standardize_market_prices_columns(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn("region",          F.upper(F.trim(F.col("region"))))
        .withColumn("market_type",     F.upper(F.trim(F.col("market_type"))))
        .withColumn("source_system",   F.upper(F.trim(F.col("source_system"))))
        .withColumn("price_eur_mwh",   F.col("price_eur_mwh").cast("double"))
        .withColumn("volume_mwh",      F.expr("try_cast(volume_mwh as double)"))
        .withColumn("event_date",      F.to_date("event_date"))
        .withColumn("last_updated_ts", F.to_timestamp("last_updated_ts"))
        .withColumn("report_day",      F.to_date("ingestion_ts"))
        .drop("_rescued_data")
    )


def filter_invalid_market_prices_rows(df: DataFrame, rules: dict) -> DataFrame:
    return (
        df
        .filter(F.col("event_date").isNotNull())
        .filter(F.col("region").isNotNull() & (F.trim(F.col("region")) != ""))
        .filter(F.col("market_type").isNotNull() & (F.trim(F.col("market_type")) != ""))
        .filter(F.col("source_system").isNotNull())
        .filter(F.col("price_eur_mwh") >= rules["market_prices"]["min_price_eur_mwh"])
        .filter(F.col("price_eur_mwh") <= rules["market_prices"]["max_price_eur_mwh"])
        .filter(F.col("volume_mwh") >= rules["market_prices"]["min_volume_mwh"])
    )