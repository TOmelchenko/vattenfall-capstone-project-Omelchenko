from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


@udf(returnType=StringType())
def classify_duration_band(duration_minutes) -> str:
    """
    Classifies grid event duration based on standard power quality definitions.
    Instantaneous: <= 0.01 min  (< 0.5 cycles, ~10ms)
    Momentary:     <= 0.05 min  (0.5 cycles to 3 seconds)
    Temporary:     <= 1 min     (3 seconds to 1 minute)
    Sustained:     > 1 min      (requires manual intervention)
    """
    if duration_minutes is None:
        return None
    duration = float(duration_minutes)
    if duration <= 0.01:
        return "INSTANTANEOUS"
    if duration <= 0.05:
        return "MOMENTARY"
    if duration <= 1:
        return "TEMPORARY"
    return "SUSTAINED"