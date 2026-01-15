from fastapi import APIRouter, Depends
from ...schemas.user_schema import TrajectFeaturesRequest
from ml.scripts.predictor import TripPredictor
from ...db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...models.user_model import EtaPrediction

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.post("/")
def predict(traject: TrajectFeaturesRequest, db: Session = Depends(get_db)):
    predictor = TripPredictor()
    result = predictor.predict(traject)
    new_prediction = EtaPrediction(predicted_trip_duration=result)
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return {"estimated_duration": result}


@router.get("/analytics/avg-duration-by-hour")
def get_avg_duration_by_hour(db: Session = Depends(get_db)):
    query = text(
        """
        SELECT pickuphour, AVG(trip_duration) AS avg_trip_duration
        FROM silver_data
        GROUP BY pickuphour
        ORDER BY pickuphour
    """
    )
    result = db.execute(query).mappings().all()
    return result


@router.get("/analytics/payment-analysis")
def get_avg_duration_by_hour(db: Session = Depends(get_db)):
    query = text(
        """
        SELECT payment_type, COUNT(*) AS total_trips, AVG(trip_duration) AS 
        avg_duration 
        FROM silver_data 
        GROUP BY payment_type
    """
    )
    result = db.execute(query).mappings().all()
    return result
