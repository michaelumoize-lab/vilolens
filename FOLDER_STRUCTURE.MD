vinolens/
│
├── frontend/                          # Next.js 14+ (Deployed to Vercel)
│   ├── app/                           # App Router (pages & layouts)
│   ├── components/                    # UI & chart components
│   │   ├── ui/                        # Reusable primitives (buttons, inputs)
│   │   ├── wine-form.tsx              # Input chemical properties
│   │   └── prediction-card.tsx        # Prediction & Gemini explanation display
│   ├── lib/                           # API client (fetch to FastAPI backend)
│   ├── public/                        # Static assets (images, icons)
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── backend/                           # FastAPI Application (Deployed to Render / Fly.io / Docker)
│   ├── app/
│   │   ├── main.py                    # App factory, CORS, middleware, router mount
│   │   ├── config.py                  # Pydantic BaseSettings (GEMINI_API_KEY, MODEL_PATH)
│   │   ├── api/
│   │   │   ├── deps.py                # Shared dependencies (model loader, auth)
│   │   │   └── v1/
│   │   │       ├── router.py          # API v1 aggregator
│   │   │       ├── endpoints/
│   │   │       │   ├── predict.py     # POST /predict (Quality score & feature impact)
│   │   │       │   ├── cluster.py     # POST /cluster (Wine profile discovery)
│   │   │       │   ├── wines.py       # GET /wines (Dataset exploration & stats)
│   │   │       │   └── explain.py     # POST /explain (Gemini sommelier reasoning)
│   │   ├── schemas/                   # Pydantic v2 schemas
│   │   │   ├── wine.py                # WineFeaturesInput, WineStats
│   │   │   └── prediction.py          # PredictionResponse, ExplanationResponse
│   │   ├── services/                  # Core business logic
│   │   │   ├── predictor.py           # Loads sklearn pipeline and computes inference
│   │   │   ├── clusterer.py           # Unsupervised K-Means clustering service
│   │   │   └── gemini_sommelier.py    # Google Gemini API prompt & explanation engine
│   │   └── models/                    # Production model artifacts loaded by FastAPI
│   │       ├── quality_regressor.joblib
│   │       └── wine_clusters.joblib
│   │
│   ├── Dockerfile                     # Lightweight FastAPI container for deployment
│   └── .dockerignore
│
├── ml/                                # Offline ML Training & Research
│   ├── notebooks/                     # Exploratory & Prototyping
│   │   ├── 01_eda.ipynb               # Feature distributions & correlations
│   │   ├── 02_regression.ipynb        # Quality prediction experiments
│   │   └── 03_clustering.ipynb        # K-Means & PCA profiling
│   ├── src/                           # Reproducible pipeline code
│   │   ├── __init__.py
│   │   ├── data.py                    # Data loaders & validation
│   │   ├── features.py                # Scaling, transforms & feature engineering
│   │   ├── train_regression.py        # Model training script -> saves to backend/app/models/
│   │   ├── train_clustering.py        # Clustering script -> saves to backend/app/models/
│   │   └── evaluate.py                # MSE, RMSE, R2, Silhouette scores
│   └── configs/
│       └── hyperparameters.yaml       # Configurable training params
│
├── data/                              # Data storage (gitignored except raw sample)
│   ├── raw/                           # Immutable raw data (WineQT.csv)
│   └── processed/                     # Cleaned / split / scaled datasets
│
├── tests/                             # Automated Test Suite
│   ├── backend/
│   │   ├── test_api.py                # FastAPI TestClient endpoint tests
│   │   └── test_predictor.py          # Inference & Gemini mock tests
│   └── ml/
│       └── test_data_pipeline.py      # Data leakage & shape tests
│
├── .github/                           # CI/CD Workflows
│   └── workflows/
│       ├── test.yml                   # Linting & unit tests on PR
│       └── deploy.yml                 # Automated deployment
│
├── .env.example                       # Documented environment variables
├── .gitignore
├── docker-compose.yml                 # Orchestrates Frontend + Backend locally
├── pyproject.toml                     # Single unified dependency management with uv
└── README.md