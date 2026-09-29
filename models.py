from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    requirement = Column(String(20), nullable=False, default="Buy")  # Buy, Rent, Sell
    preferred_city = Column(String(50), nullable=False)
    preferred_locality = Column(String(100), nullable=False)
    preferred_bhk = Column(Integer, nullable=False, default=2)
    budget = Column(Float, nullable=False, default=5000000.0)
    property_type = Column(String(50), nullable=False, default="Apartment")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(String(30), unique=True, index=True, nullable=False)
    owner_name = Column(String(100), nullable=False)
    owner_phone = Column(String(20), nullable=False)
    property_type = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    locality = Column(String(100), nullable=False)
    bhk = Column(Integer, nullable=False)
    total_sqft = Column(Float, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    balcony = Column(Integer, nullable=False, default=1)
    floor = Column(Integer, nullable=False, default=1)
    total_floors = Column(Integer, nullable=False, default=5)
    parking = Column(Integer, nullable=False, default=1)
    furnishing_status = Column(String(30), nullable=False, default="Semi-Furnished")
    property_age = Column(Integer, nullable=False, default=2)
    facing = Column(String(20), nullable=False, default="East")
    availability = Column(String(30), nullable=False, default="Ready to Move")
    expected_price = Column(Float, nullable=False)
    predicted_price = Column(Float, nullable=True)
    fair_price = Column(Float, nullable=True)
    best_price = Column(Float, nullable=True)
    price_per_sqft = Column(Float, nullable=True)
    status = Column(String(30), nullable=False, default="Available")  # Available, Under Negotiation, Sold, Rented, Inactive
    listing_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(String(30), nullable=True)
    input_data = Column(Text, nullable=False)  # JSON string of input parameters
    predicted_price = Column(Float, nullable=False)
    fair_price = Column(Float, nullable=False)
    best_price = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
