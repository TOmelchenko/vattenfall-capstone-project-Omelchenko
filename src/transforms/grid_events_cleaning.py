from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def standardize_grid_events_columns(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn("event_id",         F.upper(F.trim(F.col("event_id"))))
        .withColumn("region",           F.upper(F.trim(F.col("region"))))
        .withColumn("asset_id",         F.upper(F.trim(F.col("asset_id"))))
        .withColumn("event_type",       F.upper(F.trim(F.col("event_type"))))
        .withColumn("severity",         F.upper(F.trim(F.col("severity"))))
        .withColumn("source_system",    F.upper(F.trim(F.col("source_system"))))
        .withColumn("duration_minutes", F.col("duration_minutes").cast("int"))
        .withColumn("event_date",       F.to_date("event_date"))
        .withColumn("last_updated_ts",  F.to_timestamp("last_updated_ts"))
    )


def filter_invalid_grid_events_rows(df: DataFrame, rules: dict) -> DataFrame:
    return (
        df
        .filter(F.col("event_id").isNotNull() & (F.trim(F.col("event_id")) != ""))
        .filter(F.col("event_date").isNotNull())
        .filter(F.col("region").isNotNull() & (F.trim(F.col("region")) != ""))
        .filter(F.col("asset_id").isNotNull() & (F.trim(F.col("asset_id")) != ""))
        .filter(F.col("event_type").isNotNull())
        .filter(F.col("duration_minutes") >= 0)
        .filter(F.col("duration_minutes") <= rules["grid_events"]["max_duration_minutes"])
    )