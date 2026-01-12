from fastapi import APIRouter
from ...schemas.user_schema import TrajectFeaturesRequest
from ml.scripts.predictor import TripPredictor

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.post("/")
def predict(traject: TrajectFeaturesRequest):
    predictor = TripPredictor()

    result = predictor.predict(traject)

    return {"estimated_duration": result}


# {
#     "trip_distance": 1.6,
#     "fare_amount": 10.0,
#     "tip_amount": 3.0,
#     "tolls_amount": 0.0,
#     "total_amount": 18.0,
#     "Airport_fee": 0.0,
#     "RatecodeID": 1,
#     "pickuphour": 0,
#     "dayof_week": 4,
# }
