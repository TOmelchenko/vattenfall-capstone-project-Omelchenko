from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def classify_price_band(price_eur_mwh) -> str:
    if price_eur_mwh is None:
        return None
    price = float(price_eur_mwh)
    if price < 30:
        return "LOW"
    if price < 80:
        return "MEDIUM"
    return "HIGH"