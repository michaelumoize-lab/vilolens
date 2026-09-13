from pathlib import Path
import joblib
import pandas as pd
from backend.app.schemas.wine import WineFeaturesInput

# Path to the exported production model artifact
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "backend" / "app" / "models" / "quality_model.joblib"


class WinePredictor:
    """Service class responsible for loading the ML pipeline and generating predictions."""

    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the saved joblib pipeline into memory once at startup."""
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at: {self.model_path}. "
                "Please run `uv run python ml/src/train_regression.py` first."
            )
        self.model = joblib.load(self.model_path)
        print(f"[PredictorService] Loaded model from: {self.model_path}")

    def predict(self, features: WineFeaturesInput) -> float:
        """
        Convert validated Pydantic features into a DataFrame matching
        the exact column names expected by Scikit-Learn, then run inference.
        """
        # Map snake_case schema field names back to dataset column names with spaces
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

        # Format as a single-row DataFrame
        input_df = pd.DataFrame([feature_dict])

        # Run prediction through the Pipeline (StandardScaler + LinearRegression)
        prediction = float(self.model.predict(input_df)[0])
        return round(prediction, 2)


# Instantiate a singleton predictor service for the application
predictor_service = WinePredictor()
