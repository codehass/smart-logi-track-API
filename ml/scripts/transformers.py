from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name


def load_and_save_bronze(input_path, output_path):
    spark = SparkSession.builder.getOrCreate()

    df = spark.read.format("parquet").load(input_path)

    from pyspark.sql.functions import current_timestamp, input_file_name

    df_bronze = df.withColumn("ingestion_timestamp", current_timestamp()).withColumn(
        "source_file", input_file_name()
    )

    # Use coalesce(1) to merge all data into one partition
    # Note: I changed format back to "parquet" based on your request
    df_bronze.coalesce(1).write.mode("overwrite").format("parquet").save(output_path)

    return df_bronze
