from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.wine import WineFeaturesInput, PredictionResponse
from backend.app.services.predictor import predictor_service

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Wine Quality",
    description="Accepts 11 physicochemical wine measurements and predicts quality rating using the trained ML model."
)
def predict_wine_quality(wine_input: WineFeaturesInput) -> PredictionResponse:
    """Endpoint to run quality prediction on incoming wine features."""
    try:
        predicted_score = predictor_service.predict(wine_input)
        rounded_score = int(round(predicted_score))

        return PredictionResponse(
            predicted_quality=predicted_score,
            rounded_quality=rounded_score,
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )
