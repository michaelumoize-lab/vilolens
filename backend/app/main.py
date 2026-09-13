from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints.predict import router as predict_router

app = FastAPI(
    title="🍷 VinoLens API",
    version="1.0.0",
    description="Machine Learning API for wine intelligence, quality prediction, and profile analysis.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS so Next.js (http://localhost:3000) can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 routes
app.include_router(predict_router, prefix="/api/v1", tags=["Predictions"])


@app.get("/", tags=["Health"])
def root():
    """Root endpoint providing general API information."""
    return {
        "project": "VinoLens",
        "status": "online",
        "docs_url": "/docs",
        "predict_endpoint": "/api/v1/predict"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Healthcheck endpoint for monitoring uptime."""
    return {"status": "healthy"}
