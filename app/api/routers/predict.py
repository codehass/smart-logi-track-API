from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction routes"])


@router.post("/predict")
def predict():
    return {"message": "Hello"}
