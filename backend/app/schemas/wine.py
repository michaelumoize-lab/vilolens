from pydantic import BaseModel, Field


class WineFeaturesInput(BaseModel):
    """Input schema representing the 11 physicochemical wine properties."""
    fixed_acidity: float = Field(..., ge=0.0, le=20.0, description="Fixed acidity (g/dm³)", example=7.4)
    volatile_acidity: float = Field(..., ge=0.0, le=2.0, description="Volatile acidity (g/dm³)", example=0.7)
    citric_acid: float = Field(..., ge=0.0, le=2.0, description="Citric acid (g/dm³)", example=0.0)
    residual_sugar: float = Field(..., ge=0.0, le=50.0, description="Residual sugar (g/dm³)", example=1.9)
    chlorides: float = Field(..., ge=0.0, le=1.0, description="Chlorides / salt content (g/dm³)", example=0.076)
    free_sulfur_dioxide: float = Field(..., ge=0.0, le=100.0, description="Free sulfur dioxide (mg/dm³)", example=11.0)
    total_sulfur_dioxide: float = Field(..., ge=0.0, le=400.0, description="Total sulfur dioxide (mg/dm³)", example=34.0)
    density: float = Field(..., ge=0.9, le=1.1, description="Density (g/cm³)", example=0.9978)
    pH: float = Field(..., ge=2.0, le=5.0, description="pH level of the wine", example=3.51)
    sulphates: float = Field(..., ge=0.0, le=3.0, description="Sulphates (g/dm³)", example=0.56)
    alcohol: float = Field(..., ge=5.0, le=20.0, description="Alcohol percentage (%)", example=9.4)


class PredictionResponse(BaseModel):
    """Output schema for model prediction response."""
    predicted_quality: float = Field(..., description="Estimated quality score (3.0 - 8.0)")
    rounded_quality: int = Field(..., description="Rounded integer quality score")
    status: str = Field(default="success", description="Status of the prediction request")
