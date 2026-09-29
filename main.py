from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import Base, engine
from app.routes import prediction, properties, clients, dashboard
from app.ml.generate_dataset import ensure_dataset_exists
from app.ml.predictor import get_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup lifespan event: setup database and initialize ML model."""
    print("=" * 60)
    print(f" Starting {settings.PROJECT_NAME} ")
    print("=" * 60)
    
    # 1. Initialize SQLite Database Tables
    Base.metadata.create_all(bind=engine)
    print("[Lifespan] Database tables verified/created.")

    # 2. Ensure synthetic dataset exists
    ensure_dataset_exists()

    # 3. Pre-load/Train ML model
    get_model()
    print("[Lifespan] ML Model initialized and ready for inference.")

    yield
    print("[Lifespan] Server shutdown cleanly.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-stack AI-powered Real Estate House Price Prediction & Smart Property Management Platform.",
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(prediction.router)
app.include_router(properties.router)
app.include_router(clients.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {
        "app_name": settings.PROJECT_NAME,
        "short_name": settings.SHORT_NAME,
        "status": "online",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ml_engine": "loaded"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
