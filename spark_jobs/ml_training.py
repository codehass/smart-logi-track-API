import argparse
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import GBTRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator


def silver_df(df, num_cols, cat_cols, target):
    """Select only the relevant columns from the Silver DataFrame."""
    selected_cols = num_cols + cat_cols + [target]
    return df.select(*selected_cols)


def main(jdbc_url, db_table, db_user, db_password, model_output_path):
    # Start Spark session
    spark = SparkSession.builder.getOrCreate()

    # Load Silver data from PostgreSQL
    df = (
        spark.read.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", db_table)
        .option("user", db_user)
        .option("password", db_password)
        .option("driver", "org.postgresql.Driver")
        .load()
    )

    # Columns
    num_cols = [
        "trip_distance",
        "fare_amount",
        "tip_amount",
        "tolls_amount",
        "total_amount",
        "Airport_fee",
    ]
    cat_cols = ["RatecodeID", "pickuphour", "dayof_week"]
    target = "trip_duration"

    df_silver = silver_df(df, num_cols, cat_cols, target)

    # Preprocessing pipeline
    indexers = [
        StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep")
        for c in cat_cols
    ]
    encoders = [
        OneHotEncoder(inputCol=f"{c}_idx", outputCol=f"{c}_ohe") for c in cat_cols
    ]
    assembler = VectorAssembler(
        inputCols=num_cols + [f"{c}_ohe" for c in cat_cols], outputCol="features"
    )

    # Split data
    train_df, test_df = df_silver.randomSplit([0.8, 0.2], seed=42)

    # Model
    model = GBTRegressor(
        featuresCol="features", labelCol=target, maxIter=50, maxDepth=5
    )

    pipeline = Pipeline(stages=indexers + encoders + [assembler, model])

    # Train
    pipeline_model = pipeline.fit(train_df)

    # Evaluate
    predictions = pipeline_model.transform(test_df)
    evaluator = RegressionEvaluator(
        labelCol=target, predictionCol="prediction", metricName="rmse"
    )
    rmse = evaluator.evaluate(predictions)
    print(f"RMSE: {rmse}")

    for metric in ["mae", "r2"]:
        evaluator.setMetricName(metric)
        print(f"{metric}: {evaluator.evaluate(predictions)}")

    # Save model
    pipeline_model.write().overwrite().save(model_output_path)
    print(f"Model saved to: {model_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jdbc-url", required=True, help="JDBC URL to PostgreSQL")
    parser.add_argument("--db-table", required=True, help="Table name in PostgreSQL")
    parser.add_argument("--db-user", required=True, help="DB username")
    parser.add_argument("--db-password", required=True, help="DB password")
    parser.add_argument(
        "--model-output", required=True, help="Path to save trained model"
    )
    args = parser.parse_args()

    main(
        jdbc_url=args.jdbc_url,
        db_table=args.db_table,
        db_user=args.db_user,
        db_password=args.db_password,
        model_output_path=args.model_output,
    )
