"""
VinoLens - Linear Regression Training Pipeline
==============================================
Loads raw wine data, performs train/test split, standardizes features,
trains a Linear Regression pipeline, evaluates metrics, and exports
the production model artifact for the FastAPI backend.
"""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Define project directory paths dynamically
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "WineQT.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_OUTPUT_PATH = BASE_DIR / "backend" / "app" / "models" / "quality_model.joblib"


def load_data(filepath: Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load dataset, clean unnecessary columns, and separate X and y."""
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at: {filepath}")

    df = pd.read_csv(filepath)

    # Drop database index column if present
    if "Id" in df.columns:
        df = df.drop(columns=["Id"])

    X = df.drop(columns=["quality"])
    y = df["quality"]
    return X, y


def export_processed_splits(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    output_dir: Path,
) -> None:
    """Save train and test splits to data/processed for data lineage and testing."""
    output_dir.mkdir(parents=True, exist_ok=True)

    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    train_df.to_csv(output_dir / "train_wine_samples.csv", index=False)
    test_df.to_csv(output_dir / "test_wine_samples.csv", index=False)
    print(f"Exported processed train and test datasets to: {output_dir}")


def build_pipeline() -> Pipeline:
    """Construct an end-to-end Pipeline combining scaling and regression."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", LinearRegression())
    ])


def evaluate_model(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    """Compute standard regression performance metrics."""
    mse = mean_squared_error(y_true, y_pred)
    metrics = {
        "MAE": mean_absolute_error(y_true, y_pred),
        "MSE": mse,
        "RMSE": np.sqrt(mse),
        "R2": r2_score(y_true, y_pred),
    }
    return metrics


def main() -> None:
    print("=" * 60)
    print("       VINOLENS: TRAINING LINEAR REGRESSION PIPELINE       ")
    print("=" * 60)

    # 1. Load Data
    print(f"Loading raw dataset from: {RAW_DATA_PATH}")
    X, y = load_data(RAW_DATA_PATH)
    print(f"Loaded {X.shape[0]} wine samples with {X.shape[1]} features.")

    # 2. Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"Split: {X_train.shape[0]} train samples, {X_test.shape[0]} test samples.")

    # Export splits to data/processed/
    export_processed_splits(X_train, X_test, y_train, y_test, PROCESSED_DIR)

    # 3. Build & Fit Pipeline
    pipeline = build_pipeline()
    print("Training Pipeline (StandardScaler + LinearRegression)...")
    pipeline.fit(X_train, y_train)

    # 4. Evaluate on Test Set
    y_pred = pipeline.predict(X_test)
    metrics = evaluate_model(y_test, y_pred)

    print("\n--- Model Evaluation Results (Test Set) ---")
    print(f"Mean Absolute Error (MAE):      {metrics['MAE']:.4f} points")
    print(f"Mean Squared Error (MSE):       {metrics['MSE']:.4f}")
    print(f"Root Mean Squared Error (RMSE): {metrics['RMSE']:.4f} points")
    print(f"R-squared Score (R²):           {metrics['R2']:.4f} ({metrics['R2']*100:.1f}%)")

    # 5. Save Artifact for FastAPI
    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_OUTPUT_PATH)
    print(f"\nProduction model artifact saved to:\n  {MODEL_OUTPUT_PATH}")
    print("=" * 60)
    print("Pipeline executed successfully!")


if __name__ == "__main__":
    main()
