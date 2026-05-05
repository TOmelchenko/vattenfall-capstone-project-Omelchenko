from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


@udf(returnType=StringType())
def classify_wind_class(wind_speed_kmh) -> str:
    """
    Classifies wind speed into IEC Wind Classes based on annual average wind speed.
    Input is in km/h, converted to m/s for IEC classification.
    IEC Class I  (High Wind):      > 8.5 m/s  (> 30.6 km/h)
    IEC Class II (Medium Wind):    6.0 - 8.5 m/s (21.6 - 30.6 km/h)
    IEC Class III (Low Wind):      5.0 - 6.0 m/s (18.0 - 21.6 km/h)
    IEC Class IV (Very Low Wind):  <= 5.0 m/s (<= 18.0 km/h)
    """
    if wind_speed_kmh is None:
        return None
    speed_ms = float(wind_speed_kmh) / 3.6
    if speed_ms > 8.5:
        return "CLASS_I_HIGH"
    if speed_ms > 6.0:
        return "CLASS_II_MEDIUM"
    if speed_ms > 5.0:
        return "CLASS_III_LOW"
    return "CLASS_IV_VERY_LOW"