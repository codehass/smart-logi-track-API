from pyspark.sql import Row, SparkSession
from pyspark.ml import Pipeline


class TripPredictor:
    def __init__(self, model_path):
        self.spark = SparkSession.builder.appName("TripBackend").getOrCreate()

        self.model = Pipeline.load(model_path)

    def predict(self, data_dict):

        df_test = self.spark.createDataFrame(Row(**data_dict))
        predictions = self.model.transform(df_test)

        return predictions.select("prediction").collect()[0]["prediction"]


predictor = TripPredictor("./models/trip_duration_model")

result = predictor.predict(
    {
        "trip_distance": 1.6,
        "fare_amount": 10.0,
        "tip_amount": 3.0,
        "tolls_amount": 0.0,
        "total_amount": 18.0,
        "Airport_fee": 0.0,
        "RatecodeID": 1,
        "pickuphour": 0,
        "dayof_week": 4,
    }
)

print(result)
