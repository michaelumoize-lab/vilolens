# 🍷 VinoLens

> **An AI-powered wine intelligence platform that uses machine learning to analyze wine chemistry, predict quality, discover wine profiles, and explain predictions with Google Gemini.**

VinoLens is a full-stack machine learning project built around the **Wine Quality dataset**. It combines classical machine learning with a modern web application and generative AI.

The goal isn't simply to predict a wine's quality score — VinoLens aims to help users understand **why** a wine receives its prediction and discover patterns across different wine profiles.

---

## ✨ Features

### 🍷 Wine Quality Prediction

Enter the physicochemical properties of a wine and receive a predicted quality score.

* Linear Regression / other ML models
* Model evaluation and comparison
* Quality prediction from wine chemistry
* Feature analysis

### 📊 Wine Explorer

Explore the dataset interactively.

* Visualize relationships between wine properties
* Filter wines by characteristics
* Explore quality distributions
* Compare different wine profiles

### 🧠 Wine Profile Discovery

Use **unsupervised learning** to discover naturally occurring groups of wines.

Using clustering algorithms such as K-Means, VinoLens can identify wine profiles based on their chemical characteristics without using the quality label.

### 🔍 Model Insights

Understand what influences predictions.

* Feature importance
* Feature correlations
* Prediction analysis
* Model performance metrics

### 🤖 Gemini AI Sommelier

Google Gemini provides a natural-language explanation of the ML model's prediction.

Instead of simply showing:

> **Predicted Quality: 7.2**

VinoLens can explain:

> The wine's relatively high alcohol and sulphate levels contribute positively to the predicted quality, while volatile acidity has a negative influence.

**The ML model makes the prediction. Gemini explains it.**

---

## 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │     Next.js     │
                         │    Frontend     │
                         └────────┬────────┘
                                  │
                              HTTP / REST
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         │     Backend     │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ ML Model │ │ K-Means  │ │  Gemini  │
              │Regression│ │Clustering│ │   AI     │
              └──────────┘ └──────────┘ └──────────┘
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Wine Quality    │
                         │ Dataset         │
                         └─────────────────┘
```

---

## 🧰 Tech Stack

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Jupyter Notebook

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### AI

* Google Gemini API

### Development / Deployment

* Git
* GitHub
* Docker
* Docker Compose

---

## 📁 Project Structure

```text
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
```

---

## 📊 Dataset

VinoLens uses the **Wine Quality dataset** containing physicochemical measurements of wine along with a quality score.

### Input Features

The model can use features such as:

| Feature                | Description               |
| ---------------------- | ------------------------- |
| `fixed acidity`        | Fixed acids in the wine   |
| `volatile acidity`     | Volatile acidity          |
| `citric acid`          | Citric acid concentration |
| `residual sugar`       | Remaining sugar           |
| `chlorides`            | Salt concentration        |
| `free sulfur dioxide`  | Free sulfur dioxide       |
| `total sulfur dioxide` | Total sulfur dioxide      |
| `density`              | Density of the wine       |
| `pH`                   | Acidity level             |
| `sulphates`            | Sulphate concentration    |
| `alcohol`              | Alcohol percentage        |

### Target

```text
quality
```

The quality score is an integer rating assigned to each wine.

---

## 🤖 Machine Learning

VinoLens explores the dataset through multiple machine learning approaches.

### Supervised Learning

The initial model treats wine quality as a regression problem:

```text
Wine Chemistry
      │
      ▼
Machine Learning Model
      │
      ▼
Predicted Quality
```

Example:

```text
Input → Wine chemical properties

Output → 7.2 / 10
```

Future versions can also treat the problem as classification:

```text
quality >= 7 → Good
quality < 7  → Not Good
```

---

## 🔬 Unsupervised Learning

VinoLens also explores the dataset without using the `quality` label.

K-Means clustering can identify groups of wines with similar chemical characteristics.

```text
Wine Data
    │
    ▼
K-Means
    │
    ├── Cluster 1
    ├── Cluster 2
    └── Cluster 3
```

This allows VinoLens to answer questions such as:

> "What types of wines naturally occur in this dataset?"

---

## 🧠 Gemini Integration

Google Gemini is used as an **explanation layer**, rather than replacing the machine learning model.

```text
Wine Features
      │
      ▼
ML Model
      │
      ├── Prediction
      ├── Feature influence
      └── Cluster
             │
             ▼
          Gemini
             │
             ▼
     Human-readable explanation
```

This separation keeps the ML prediction deterministic and allows Gemini to focus on communicating the results.

---

## 🚀 Development Roadmap

### Phase 1 — Data Exploration

* [x] Obtain Wine Quality dataset
* [ ] Load dataset with Pandas
* [ ] Explore statistics
* [ ] Check missing values
* [ ] Visualize distributions
* [ ] Analyze feature correlations

### Phase 2 — First ML Model

* [ ] Prepare features and target
* [ ] Train/test split
* [ ] Implement linear regression
* [ ] Evaluate MSE
* [ ] Evaluate RMSE
* [ ] Evaluate R²
* [ ] Experiment with different features

### Phase 3 — Advanced ML

* [ ] Try additional regression models
* [ ] Compare model performance
* [ ] Implement classification
* [ ] Implement K-Means clustering
* [ ] Investigate feature importance
* [ ] Improve preprocessing

### Phase 4 — FastAPI

* [ ] Create FastAPI application
* [ ] Create `/predict` endpoint
* [ ] Create `/clusters` endpoint
* [ ] Create `/statistics` endpoint
* [ ] Load trained ML models
* [ ] Add request validation

### Phase 5 — Next.js

* [ ] Build landing page
* [ ] Create wine analysis form
* [ ] Build prediction dashboard
* [ ] Add interactive charts
* [ ] Build wine explorer
* [ ] Add clustering visualization
* [ ] Add responsive design

### Phase 6 — Gemini

* [ ] Integrate Gemini API
* [ ] Generate prediction explanations
* [ ] Explain influential features
* [ ] Generate wine profile summaries

### Phase 7 — Production

* [ ] Dockerize application
* [ ] Add environment configuration
* [ ] Add automated tests
* [ ] Deploy frontend
* [ ] Deploy backend
* [ ] Document API
* [ ] Add CI/CD

---

## 🎯 Example User Flow

```text
1. User opens VinoLens
             ↓
2. Selects "Analyze Wine"
             ↓
3. Enters wine chemistry
             ↓
4. FastAPI receives request
             ↓
5. ML model generates prediction
             ↓
6. Model determines wine profile
             ↓
7. Gemini explains the result
             ↓
8. User sees:
   
   Quality: 7.2 / 10
   Profile: High-Alcohol Balanced
   
   + Positive factors
   - Negative factors
   💡 AI explanation
```

---

## 🔮 Future Ideas

Potential future improvements include:

* Wine recommendation system
* Similar-wine search
* "Find wines similar to this one"
* User accounts and saved analyses
* Prediction history
* Wine comparison
* Interactive what-if analysis
* SHAP-based model explanations
* Experiment tracking
* Model versioning
* Additional wine datasets
* Red vs. white wine analysis
* Personalized wine recommendations

---

## ⚠️ Disclaimer

VinoLens is an educational machine learning project.

The predictions represent patterns learned from the dataset and should not be interpreted as professional wine certification, laboratory analysis, or expert sommelier judgment.

---

## 📚 Learning Goals

This project is designed to demonstrate practical understanding of:

* Supervised learning
* Regression
* Classification
* Unsupervised learning
* Clustering
* Feature engineering
* Model evaluation
* Data visualization
* REST APIs
* Full-stack development
* Generative AI integration
* ML model deployment

---

## 👨‍💻 Project Status

🚧 **Currently in development**

The project is being developed incrementally alongside the study of machine learning concepts.

### Current focus

> **Data exploration → Linear Regression → Model Evaluation**

---

## 📄 License

This project is intended for educational and portfolio purposes.
