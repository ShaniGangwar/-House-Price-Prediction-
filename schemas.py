from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

# ==================== PREDICTION SCHEMAS ====================

class PredictionInput(BaseModel):
    city: str = Field(..., example="Delhi")
    locality: str = Field(..., example="Connaught Place")
    property_type: str = Field("Apartment", example="Apartment")
    bhk: int = Field(2, ge=1, description="Number of BHK, min 1")
    total_sqft: float = Field(1200.0, ge=100.0, description="Area in sq.ft., min 100")
    bathrooms: int = Field(2, ge=1, description="Bathrooms count, min 1")
    balcony: int = Field(1, ge=0, description="Balconies count")
    floor: int = Field(3, ge=0, description="Floor number")
    total_floors: int = Field(8, ge=1, description="Total building floors")
    parking: int = Field(1, ge=0, description="Parking spots count")
    furnishing_status: str = Field("Semi-Furnished", example="Semi-Furnished")
    property_age: int = Field(5, ge=0, description="Property age in years")
    facing: str = Field("East", example="East")
    availability: str = Field("Ready to Move", example="Ready to Move")

class PredictionResponse(BaseModel):
    predicted_price: float
    fair_price: float
    best_price: float
    minimum_reasonable_price: float
    maximum_reasonable_price: float
    price_per_sqft: float
    confidence_score: float
    recommendation: str
    message: str

class BHKComparisonItem(BaseModel):
    bhk: str
    bhk_number: int
    estimated_price: float
    price_per_sqft: float
    recommended_budget: float

class BHKComparisonResponse(BaseModel):
    city: str
    locality: str
    total_sqft: float
    comparisons: List[BHKComparisonItem]

class ModelMetricsResponse(BaseModel):
    algorithm: str
    mae: float
    rmse: float
    r2_score: float
    train_samples: int
    test_samples: int
    trained_at: str
    feature_importance: Dict[str, float]

# ==================== CLIENT SCHEMAS ====================

class ClientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=7, max_length=20)
    email: Optional[str] = None
    requirement: str = Field("Buy", example="Buy")
    preferred_city: str = Field(..., min_length=1)
    preferred_locality: str = Field(..., min_length=1)
    preferred_bhk: int = Field(2, ge=1)
    budget: float = Field(5000000.0, ge=0)
    property_type: str = Field("Apartment")
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    requirement: Optional[str] = None
    preferred_city: Optional[str] = None
    preferred_locality: Optional[str] = None
    preferred_bhk: Optional[int] = None
    budget: Optional[float] = None
    property_type: Optional[str] = None
    notes: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== PROPERTY SCHEMAS ====================

class PropertyBase(BaseModel):
    owner_name: str = Field(..., min_length=2)
    owner_phone: str = Field(..., min_length=7)
    property_type: str = Field("Apartment")
    city: str = Field(..., min_length=1)
    locality: str = Field(..., min_length=1)
    bhk: int = Field(2, ge=1)
    total_sqft: float = Field(1200.0, ge=100.0)
    bathrooms: int = Field(2, ge=1)
    balcony: int = Field(1, ge=0)
    floor: int = Field(3, ge=0)
    total_floors: int = Field(8, ge=1)
    parking: int = Field(1, ge=0)
    furnishing_status: str = Field("Semi-Furnished")
    property_age: int = Field(5, ge=0)
    facing: str = Field("East")
    availability: str = Field("Ready to Move")
    expected_price: float = Field(..., ge=0)
    status: str = Field("Available")

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    property_type: Optional[str] = None
    city: Optional[str] = None
    locality: Optional[str] = None
    bhk: Optional[int] = None
    total_sqft: Optional[float] = None
    bathrooms: Optional[int] = None
    balcony: Optional[int] = None
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    parking: Optional[int] = None
    furnishing_status: Optional[str] = None
    property_age: Optional[int] = None
    facing: Optional[str] = None
    availability: Optional[str] = None
    expected_price: Optional[float] = None
    status: Optional[str] = None

class PropertyResponse(PropertyBase):
    id: int
    property_id: str
    predicted_price: Optional[float] = None
    fair_price: Optional[float] = None
    best_price: Optional[float] = None
    price_per_sqft: Optional[float] = None
    listing_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# ==================== DASHBOARD & ANALYTICS SCHEMAS ====================

class DashboardStatsResponse(BaseModel):
    total_properties: int
    available_properties: int
    sold_properties: int
    rented_properties: int
    under_negotiation_properties: int
    total_clients: int
    average_property_price: float
    average_predicted_price: float
    average_price_per_sqft: float
    total_predictions: int

class DashboardChartsResponse(BaseModel):
    properties_by_bhk: List[Dict[str, Any]]
    properties_by_city: List[Dict[str, Any]]
    properties_by_locality: Optional[List[Dict[str, Any]]] = None
    price_distribution: List[Dict[str, Any]]
    property_status: List[Dict[str, Any]]
    average_price_by_bhk: List[Dict[str, Any]]
    monthly_listings: List[Dict[str, Any]]

