import argparse
import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name


def save_as_single_parquet(df, output_filename):
    temp_dir = "/tmp/temp_spark_out"

    df.coalesce(1).write.mode("overwrite").parquet(temp_dir)

    part_files = [
        f
        for f in os.listdir(temp_dir)
        if f.startswith("part-") and f.endswith(".parquet")
    ]
    if not part_files:
        raise FileNotFoundError(f"No parquet part file found in {temp_dir}")

    part_file = part_files[0]

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    shutil.move(os.path.join(temp_dir, part_file), output_filename)
    shutil.rmtree(temp_dir)

    print(f"Saved parquet file to: {output_filename}")


def load_and_save_bronze(input_path, output_filename):
    spark = SparkSession.builder.getOrCreate()

    df = spark.read.format("parquet").load(input_path)

    df_bronze = df.withColumn("ingestion_timestamp", current_timestamp()).withColumn(
        "source_file", input_file_name()
    )

    save_as_single_parquet(df_bronze, output_filename)

    return df_bronze


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df_bronze = load_and_save_bronze(args.input, args.output)
