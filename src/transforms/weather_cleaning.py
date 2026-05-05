from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def standardize_weather_columns(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn("region",              F.upper(F.trim(F.col("region"))))
        .withColumn("weather_alert_level", F.upper(F.trim(F.col("weather_alert_level"))))
        .withColumn("source_system",       F.upper(F.trim(F.col("source_system"))))
        .withColumn("temperature_c",       F.col("temperature_c").cast("double"))
        .withColumn("wind_speed_kmh",      F.col("wind_speed_kmh").cast("double"))
        .withColumn("precipitation_mm",    F.col("precipitation_mm").cast("double"))
        .withColumn("event_date",          F.to_date("event_date"))
        .withColumn("last_updated_ts",     F.to_timestamp("last_updated_ts"))
    )


def filter_invalid_weather_rows(df: DataFrame, rules: dict) -> DataFrame:
    return (
        df
        .filter(F.col("event_date").isNotNull())
        .filter(F.col("region").isNotNull() & (F.trim(F.col("region")) != ""))
        .filter(F.col("temperature_c").isNotNull())
        .filter(F.col("temperature_c") >= rules["weather"]["min_temperature_c"])
        .filter(F.col("temperature_c") <= rules["weather"]["max_temperature_c"])
        .filter(F.col("wind_speed_kmh") >= 0)
        .filter(F.col("wind_speed_kmh") <= rules["weather"]["max_wind_speed_kmh"])
        .filter(F.col("precipitation_mm") >= 0)
    )