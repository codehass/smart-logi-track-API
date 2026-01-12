from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.abspath(
    os.path.join(script_dir, "..", "models", "trip_duration_model")
)


class TripPredictor:
    def __init__(self):
        self.spark = SparkSession.builder.appName("TripBackend").getOrCreate()
        self.model = PipelineModel.load(model_path)

    def predict(self, data_dict):
        df_test = self.spark.createDataFrame([data_dict])
        predictions = self.model.transform(df_test)
        return predictions.select("prediction").first()["prediction"]


# predictor = TripPredictor(model_path)

# result = predictor.predict(
#     {
#         "trip_distance": 1.6,
#         "fare_amount": 10.0,
#         "tip_amount": 3.0,
#         "tolls_amount": 0.0,
#         "total_amount": 18.0,
#         "Airport_fee": 0.0,
#         "RatecodeID": 1,
#         "pickuphour": 0,
#         "dayof_week": 4,
#     }
# )

# print("Predicted trip duration (min):", result)
