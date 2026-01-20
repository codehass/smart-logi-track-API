import os
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, round, hour, dayofweek, month

db_user = os.getenv("DATABASE_USER")
db_pass = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")
db_host = os.getenv("DATABASE_HOST")
db_port = os.getenv("DATABASE_PORT")


def clean_and_save_silver_df(df):
    df = df.drop("ingestion_timestamp", "source_file")
    df = df.na.drop(how="any")
    df = df.withColumn(
        "trip_duration",
        (
            unix_timestamp(col("tpep_dropoff_datetime"))
            - unix_timestamp(col("tpep_pickup_datetime"))
        )
        / 60,
    )
    df = df.withColumn("trip_duration", round(col("trip_duration"), 2))
    df = df.filter(col("passenger_count") > 0)
    df = df.filter((col("trip_distance") > 0) & (col("trip_distance") < 200))
    df = df.filter((col("trip_duration") > 0) & (col("trip_duration") <= 120))
    df = df.filter((col("fare_amount") > 0) & (col("fare_amount") <= 500))
    df = (
        df.withColumn("pickuphour", hour("tpep_pickup_datetime"))
        .withColumn("dayof_week", dayofweek("tpep_pickup_datetime"))
        .withColumn("month", month("tpep_pickup_datetime"))
    )
    df = df.filter(col("RateCodeID") != 99)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to Bronze parquet")
    args = parser.parse_args()

    spark = SparkSession.builder.getOrCreate()

    df_bronze = spark.read.format("parquet").load(args.input)
    df_silver = clean_and_save_silver_df(df_bronze)

    POSTGRES_URL = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"
    POSTGRES_PROPERTIES = {
        "user": db_user,
        "password": db_pass,
        "driver": "org.postgresql.Driver",
    }
    POSTGRES_TABLE = "silver_data"

    df_silver.write.jdbc(
        url=POSTGRES_URL,
        table=POSTGRES_TABLE,
        mode="overwrite",
        properties=POSTGRES_PROPERTIES,
    )

    print(f"Saved Silver data to Postgres table: {POSTGRES_TABLE}")
