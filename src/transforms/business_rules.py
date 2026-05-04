from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def add_market_prices_flags(df: DataFrame, rules: dict) -> DataFrame:
    return (
        df
        .withColumn(
            "is_high_price",
            F.when(F.col("price_eur_mwh") >= rules["market_prices"]["high_price_threshold"], 1).otherwise(0)
        )
    )  