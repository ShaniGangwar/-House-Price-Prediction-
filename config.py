import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "AI House Price Predictor & Smart Property Management System"
    SHORT_NAME: str = "SmartHouse AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Paths
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    DATASET_PATH: Path = DATA_DIR / "housing_data.csv"
    MODEL_PATH: Path = MODELS_DIR / "house_price_model.joblib"
    METRICS_PATH: Path = MODELS_DIR / "house_price_model_metrics.json"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./realestate.db")
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)
