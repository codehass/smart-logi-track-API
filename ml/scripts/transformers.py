import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name


def save_as_single_parquet(df, output_filename):
    """
    Saves a Spark DataFrame as a single parquet file with a specific name.
    """
    temp_dir = "temp_spark_out"

    df.coalesce(1).write.mode("overwrite").parquet(temp_dir)

    part_file = [
        f
        for f in os.listdir(temp_dir)
        if f.startswith("part-") and f.endswith(".parquet")
    ][0]

    if os.path.exists(output_filename):
        os.remove(output_filename)

    shutil.move(os.path.join(temp_dir, part_file), output_filename)

    shutil.rmtree(temp_dir)

    print(f"Saved: {output_filename}")


def load_and_save_bronze(input_path, output_filename):
    spark = SparkSession.builder.getOrCreate()

    df = spark.read.format("parquet").load(input_path)

    df_bronze = df.withColumn("ingestion_timestamp", current_timestamp()).withColumn(
        "source_file", input_file_name()
    )

    save_as_single_parquet(df_bronze, output_filename)

    return df_bronze
