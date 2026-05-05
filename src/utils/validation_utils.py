"""
validation_utils.py
Reusable validation logic for bronze, silver, and gold notebooks.
"""

import logging
from pyspark.sql.utils import AnalysisException
from pyspark.sql import functions as F


def get_logger(level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    return logging.getLogger(__name__)


def check_existence(spark, table: str, log) -> bool:
    try:
        spark.table(table)
        log.info(f"[EXISTS]   {table} found.")
        return True
    except AnalysisException:
        log.error(f"[MISSING]  Table not found: {table}")
        return False


def check_row_count(spark, table: str, log) -> tuple:
    row_count = spark.table(table).count()
    if row_count > 0:
        log.info(f"[ROWS]     {table} has {row_count} rows.")
        return "PASSED", str(row_count)
    else:
        log.error(f"[ROWS]     {table} is empty.")
        return "FAILED", "0"


def check_schema(spark, table: str, required_columns: set, log) -> tuple:
    actual_columns  = set(spark.table(table).columns)
    missing_columns = required_columns - actual_columns
    if missing_columns:
        log.error(f"[SCHEMA]   {table} missing columns: {missing_columns}")
        return "FAILED", str(missing_columns)
    else:
        log.info(f"[SCHEMA]   {table} schema OK.")
        return "PASSED", ""


def check_nulls(spark, table: str, key_columns: list, log) -> list:
    df = spark.table(table)
    results = []
    for col_name in key_columns:
        null_count = df.filter(F.col(col_name).isNull()).count()
        if null_count > 0:
            log.error(f"[NULLS]    {table}.{col_name} has {null_count} null values.")
            results.append((f"nulls_{col_name}", "FAILED", str(null_count)))
        else:
            log.info(f"[NULLS]    {table}.{col_name} OK.")
            results.append((f"nulls_{col_name}", "PASSED", "0"))
    return results


def check_negatives(spark, table: str, numeric_checks: list, log) -> list:
    df = spark.table(table)
    results = []
    for col_name, min_val in numeric_checks:
        neg_count = df.filter(F.col(col_name) < min_val).count()
        if neg_count > 0:
            log.error(f"[NEGATIVE] {table}.{col_name} has {neg_count} values below {min_val}.")
            results.append((f"negative_{col_name}", "FAILED", str(neg_count)))
        else:
            log.info(f"[NEGATIVE] {table}.{col_name} OK.")
            results.append((f"negative_{col_name}", "PASSED", "0"))
    return results


def check_business_rules(spark, table: str, col_name: str, valid_values: list, log) -> tuple:
    invalid_count = spark.table(table).filter(
        ~F.col(col_name).isin(valid_values)
    ).count()
    if invalid_count > 0:
        log.error(f"[RULE]     {table}.{col_name} has {invalid_count} invalid values. Expected: {valid_values}")
        return f"rule_{col_name}", "FAILED", str(invalid_count)
    else:
        log.info(f"[RULE]     {table}.{col_name} OK - only {valid_values} present.")
        return f"rule_{col_name}", "PASSED", "0"


def run_table_validation(spark, expected_schemas: dict, log) -> tuple:
    """
    Runs existence, row count, schema, null, and negative checks
    for all tables in expected_schemas.

    Returns (results list, validation_passed bool).
    """
    results = []
    validation_passed = True

    for table, config in expected_schemas.items():
        log.info(f"--- Validating: {table} ---")

        # existence
        if not check_existence(spark, table, log):
            validation_passed = False
            results.append({"table": table, "check": "existence", "status": "FAILED", "value": ""})
            continue
        results.append({"table": table, "check": "existence", "status": "PASSED", "value": ""})

        # row count
        status, value = check_row_count(spark, table, log)
        results.append({"table": table, "check": "row_count", "status": status, "value": value})
        if status == "FAILED":
            validation_passed = False

        # schema
        status, value = check_schema(spark, table, config["required_columns"], log)
        results.append({"table": table, "check": "schema", "status": status, "value": value})
        if status == "FAILED":
            validation_passed = False

        # nulls
        for check, status, value in check_nulls(spark, table, config["key_columns"], log):
            results.append({"table": table, "check": check, "status": status, "value": value})
            if status == "FAILED":
                validation_passed = False

        # negatives
        for check, status, value in check_negatives(spark, table, config.get("numeric_checks", []), log):
            results.append({"table": table, "check": check, "status": status, "value": value})
            if status == "FAILED":
                validation_passed = False

    return results, validation_passed


def display_summary(spark, results: list, validation_passed: bool, layer: str) -> None:
    summary_df = spark.createDataFrame(results)
    summary_df.display()

    if not validation_passed:
        raise ValueError(f"{layer} validation failed. Check the summary above for details.")
    else:
        logging.getLogger(__name__).info(f"All {layer} validation checks passed.")