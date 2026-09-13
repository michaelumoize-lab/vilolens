from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="🍷 VinoLens Serverless API",
    version="1.0.0",
    description="Vercel Serverless Python inference endpoint for VinoLens wine quality prediction.",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model artifact
MODEL_PATH = Path(__file__).resolve().parent / "models" / "quality_model.joblib"
model = None

try:
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        print(f"[Vercel Serverless] Successfully loaded model from {MODEL_PATH}")
    else:
        print(f"[Vercel Serverless] WARNING: Model not found at {MODEL_PATH}")
except Exception as e:
    print(f"[Vercel Serverless] ERROR loading model: {e}")


class WineFeaturesInput(BaseModel):
    fixed_acidity: float = Field(..., ge=0.0, le=20.0, example=7.4)
    volatile_acidity: float = Field(..., ge=0.0, le=2.0, example=0.7)
    citric_acid: float = Field(..., ge=0.0, le=2.0, example=0.0)
    residual_sugar: float = Field(..., ge=0.0, le=50.0, example=1.9)
    chlorides: float = Field(..., ge=0.0, le=1.0, example=0.076)
    free_sulfur_dioxide: float = Field(..., ge=0.0, le=100.0, example=11.0)
    total_sulfur_dioxide: float = Field(..., ge=0.0, le=400.0, example=34.0)
    density: float = Field(..., ge=0.9, le=1.1, example=0.9978)
    pH: float = Field(..., ge=2.0, le=5.0, example=3.51)
    sulphates: float = Field(..., ge=0.0, le=3.0, example=0.56)
    alcohol: float = Field(..., ge=5.0, le=20.0, example=9.4)


class PredictionResponse(BaseModel):
    predicted_quality: float
    rounded_quality: int
    status: str = "success"


def run_inference(features: WineFeaturesInput) -> PredictionResponse:
    global model
    if model is None:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
        else:
            raise HTTPException(status_code=500, detail="Model artifact missing from serverless deployment.")

    feature_dict = {
        "fixed acidity": features.fixed_acidity,
        "volatile acidity": features.volatile_acidity,
        "citric acid": features.citric_acid,
        "residual sugar": features.residual_sugar,
        "chlorides": features.chlorides,
        "free sulfur dioxide": features.free_sulfur_dioxide,
        "total sulfur dioxide": features.total_sulfur_dioxide,
        "density": features.density,
        "pH": features.pH,
        "sulphates": features.sulphates,
        "alcohol": features.alcohol,
    }

    input_df = pd.DataFrame([feature_dict])
    pred = float(model.predict(input_df)[0])
    rounded = int(round(pred))

    return PredictionResponse(
        predicted_quality=round(pred, 2),
        rounded_quality=rounded,
        status="success"
    )


# Register routes for both /api/v1/predict and /v1/predict (to handle Vercel rewrite variations)
@app.post("/api/v1/predict", response_model=PredictionResponse)
@app.post("/v1/predict", response_model=PredictionResponse)
@app.post("/predict", response_model=PredictionResponse)
def predict(features: WineFeaturesInput):
    return run_inference(features)


@app.get("/api/health")
@app.get("/health")
def health():
    return {"status": "healthy", "service": "Vercel Serverless Python"}
