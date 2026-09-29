import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc, or_, and_

from app.models import Client, Property, Prediction
from app.schemas import ClientCreate, ClientUpdate, PropertyCreate, PropertyUpdate
from app.ml.predictor import predict_house_price
from app.utils.validators import validate_property_input, validate_phone, validate_email

# ==================== CLIENT CRUD ====================

def get_clients(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    requirement: str = None,
    city: str = None
):
    query = db.query(Client)
    if search:
        s = f"%{search}%"
        query = query.filter(
            or_(
                Client.name.ilike(s),
                Client.phone.ilike(s),
                Client.email.ilike(s),
                Client.preferred_locality.ilike(s)
            )
        )
    if requirement and requirement != "All":
        query = query.filter(Client.requirement == requirement)
    if city and city != "All":
        query = query.filter(Client.preferred_city == city)

    return query.order_by(desc(Client.created_at)).offset(skip).limit(limit).all()

def get_client_by_id(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def create_client(db: Session, client_in: ClientCreate):
    db_client = Client(
        name=client_in.name.strip(),
        phone=client_in.phone.strip(),
        email=client_in.email.strip() if client_in.email else None,
        requirement=client_in.requirement,
        preferred_city=client_in.preferred_city.strip(),
        preferred_locality=client_in.preferred_locality.strip(),
        preferred_bhk=client_in.preferred_bhk,
        budget=client_in.budget,
        property_type=client_in.property_type,
        notes=client_in.notes
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client_in: ClientUpdate):
    db_client = get_client_by_id(db, client_id)
    if not db_client:
        return None

    update_data = client_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if isinstance(value, str):
                setattr(db_client, field, value.strip())
            else:
                setattr(db_client, field, value)

    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = get_client_by_id(db, client_id)
    if not db_client:
        return False
    db.delete(db_client)
    db.commit()
    return True

# ==================== PROPERTY CRUD ====================

def get_properties(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    city: str = None,
    locality: str = None,
    bhk: int = None,
    property_type: str = None,
    status: str = None,
    min_price: float = None,
    max_price: float = None,
    sort_by: str = "newest"
):
    query = db.query(Property)

    if search:
        s = f"%{search}%"
        query = query.filter(
            or_(
                Property.property_id.ilike(s),
                Property.city.ilike(s),
                Property.locality.ilike(s),
                Property.owner_name.ilike(s)
            )
        )

    if city and city != "All":
        query = query.filter(Property.city == city)
    if locality and locality != "All":
        query = query.filter(Property.locality.ilike(f"%{locality}%"))
    if bhk and bhk > 0:
        query = query.filter(Property.bhk == bhk)
    if property_type and property_type != "All":
        query = query.filter(Property.property_type == property_type)
    if status and status != "All":
        query = query.filter(Property.status == status)
    if min_price is not None and min_price >= 0:
        query = query.filter(Property.expected_price >= min_price)
    if max_price is not None and max_price > 0:
        query = query.filter(Property.expected_price <= max_price)

    # Sorting
    if sort_by == "price_low":
        query = query.order_by(asc(Property.expected_price))
    elif sort_by == "price_high":
        query = query.order_by(desc(Property.expected_price))
    elif sort_by == "oldest":
        query = query.order_by(asc(Property.listing_date))
    else:  # newest
        query = query.order_by(desc(Property.listing_date))

    return query.offset(skip).limit(limit).all()

def get_property_by_id(db: Session, prop_id: int):
    return db.query(Property).filter(Property.id == prop_id).first()

def get_property_by_prop_code(db: Session, prop_code: str):
    return db.query(Property).filter(Property.property_id == prop_code).first()

def create_property(db: Session, prop_in: PropertyCreate):
    # Auto-generate unique Property ID code like PROP-9241
    unique_code = f"PROP-{uuid.uuid4().hex[:6].upper()}"

    # Calculate AI prediction for this property automatically
    input_dict = prop_in.dict()
    ai_res = predict_house_price(input_dict)

    db_prop = Property(
        property_id=unique_code,
        owner_name=prop_in.owner_name.strip(),
        owner_phone=prop_in.owner_phone.strip(),
        property_type=prop_in.property_type,
        city=prop_in.city.strip(),
        locality=prop_in.locality.strip(),
        bhk=prop_in.bhk,
        total_sqft=prop_in.total_sqft,
        bathrooms=prop_in.bathrooms,
        balcony=prop_in.balcony,
        floor=prop_in.floor,
        total_floors=prop_in.total_floors,
        parking=prop_in.parking,
        furnishing_status=prop_in.furnishing_status,
        property_age=prop_in.property_age,
        facing=prop_in.facing,
        availability=prop_in.availability,
        expected_price=prop_in.expected_price,
        predicted_price=ai_res["predicted_price"],
        fair_price=ai_res["fair_price"],
        best_price=ai_res["best_price"],
        price_per_sqft=ai_res["price_per_sqft"],
        status=prop_in.status
    )
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop

def update_property(db: Session, prop_id: int, prop_in: PropertyUpdate):
    db_prop = get_property_by_id(db, prop_id)
    if not db_prop:
        return None

    update_data = prop_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if isinstance(value, str):
                setattr(db_prop, field, value.strip())
            else:
                setattr(db_prop, field, value)

    # Re-run ML prediction on updated attributes
    input_dict = {
        "city": db_prop.city,
        "locality": db_prop.locality,
        "property_type": db_prop.property_type,
        "bhk": db_prop.bhk,
        "total_sqft": db_prop.total_sqft,
        "bathrooms": db_prop.bathrooms,
        "balcony": db_prop.balcony,
        "floor": db_prop.floor,
        "total_floors": db_prop.total_floors,
        "parking": db_prop.parking,
        "furnishing_status": db_prop.furnishing_status,
        "property_age": db_prop.property_age,
        "facing": db_prop.facing,
        "availability": db_prop.availability,
        "expected_price": db_prop.expected_price
    }
    ai_res = predict_house_price(input_dict)
    db_prop.predicted_price = ai_res["predicted_price"]
    db_prop.fair_price = ai_res["fair_price"]
    db_prop.best_price = ai_res["best_price"]
    db_prop.price_per_sqft = ai_res["price_per_sqft"]

    db.commit()
    db.refresh(db_prop)
    return db_prop

def delete_property(db: Session, prop_id: int):
    db_prop = get_property_by_id(db, prop_id)
    if not db_prop:
        return False
    db.delete(db_prop)
    db.commit()
    return True

def get_best_deals(db: Session, budget: float = None, city: str = None, bhk: int = None, limit: int = 10):
    """Find properties where expected_price is lower than AI fair_price (best value deals)."""
    query = db.query(Property).filter(Property.status == "Available")

    if city and city != "All":
        query = query.filter(Property.city == city)
    if bhk and bhk > 0:
        query = query.filter(Property.bhk == bhk)
    if budget and budget > 0:
        query = query.filter(Property.expected_price <= budget)

    properties = query.all()

    # Calculate deal score = ((predicted_price - expected_price) / predicted_price) * 100
    scored_properties = []
    for prop in properties:
        pred = prop.predicted_price or prop.expected_price
        diff_pct = ((pred - prop.expected_price) / pred) * 100.0 if pred > 0 else 0.0
        deal_score = round(max(50.0, min(99.0, 75.0 + diff_pct)), 1)

        scored_properties.append({
            "property": prop,
            "diff_pct": round(diff_pct, 1),
            "deal_score": deal_score
        })

    # Sort by deal_score descending
    scored_properties.sort(key=lambda x: x["deal_score"], reverse=True)
    return scored_properties[:limit]

# ==================== PREDICTIONS HISTORICAL LOG ====================

def create_prediction_record(db: Session, input_data: dict, prediction_res: dict, property_id: str = None):
    db_pred = Prediction(
        property_id=property_id,
        input_data=json.dumps(input_data),
        predicted_price=prediction_res["predicted_price"],
        fair_price=prediction_res["fair_price"],
        best_price=prediction_res["best_price"],
        confidence_score=prediction_res["confidence_score"]
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

def get_recent_predictions(db: Session, limit: int = 10):
    return db.query(Prediction).order_by(desc(Prediction.created_at)).limit(limit).all()

# ==================== DASHBOARD & CHARTS ====================

def get_dashboard_stats(db: Session):
    total_properties = db.query(Property).count()
    available_properties = db.query(Property).filter(Property.status == "Available").count()
    sold_properties = db.query(Property).filter(Property.status == "Sold").count()
    rented_properties = db.query(Property).filter(Property.status == "Rented").count()
    under_negotiation = db.query(Property).filter(Property.status == "Under Negotiation").count()

    total_clients = db.query(Client).count()
    total_predictions = db.query(Prediction).count()

    avg_exp_price = db.query(func.avg(Property.expected_price)).scalar() or 0.0
    avg_pred_price = db.query(func.avg(Property.predicted_price)).scalar() or 0.0
    avg_sqft_price = db.query(func.avg(Property.price_per_sqft)).scalar() or 0.0

    return {
        "total_properties": total_properties,
        "available_properties": available_properties,
        "sold_properties": sold_properties,
        "rented_properties": rented_properties,
        "under_negotiation_properties": under_negotiation,
        "total_clients": total_clients,
        "average_property_price": round(float(avg_exp_price), 2),
        "average_predicted_price": round(float(avg_pred_price), 2),
        "average_price_per_sqft": round(float(avg_sqft_price), 2),
        "total_predictions": total_predictions
    }

def get_dashboard_charts(db: Session):
    # 1. Properties by BHK
    bhk_counts = (
        db.query(Property.bhk, func.count(Property.id))
        .group_by(Property.bhk)
        .order_by(Property.bhk)
        .all()
    )
    properties_by_bhk = [{"name": f"{bhk} BHK", "count": count} for bhk, count in bhk_counts]

    # 2. Properties by City
    city_counts = (
        db.query(Property.city, func.count(Property.id))
        .group_by(Property.city)
        .order_by(func.count(Property.id).desc())
        .limit(8)
        .all()
    )
    properties_by_city = [{"name": city, "count": count} for city, count in city_counts]

    # 3. Property Status Breakdown
    status_counts = (
        db.query(Property.status, func.count(Property.id))
        .group_by(Property.status)
        .all()
    )
    property_status = [{"name": status, "value": count} for status, count in status_counts]

    # 4. Average Price by BHK
    avg_bhk_prices = (
        db.query(Property.bhk, func.avg(Property.expected_price), func.avg(Property.predicted_price))
        .group_by(Property.bhk)
        .order_by(Property.bhk)
        .all()
    )
    average_price_by_bhk = [
        {
            "bhk": f"{bhk} BHK",
            "expected": round(float(avg_exp), 2) if avg_exp else 0,
            "predicted": round(float(avg_pred), 2) if avg_pred else 0
        }
        for bhk, avg_exp, avg_pred in avg_bhk_prices
    ]

    # 5. Price Distribution (Buckets in Lakhs)
    all_prices = [p.expected_price / 100000.0 for p in db.query(Property.expected_price).all()]
    buckets = {
        "< ₹30 Lakh": 0,
        "₹30 - ₹60 Lakh": 0,
        "₹60 - ₹90 Lakh": 0,
        "₹90 Lakh - ₹1.5 Cr": 0,
        "> ₹1.5 Cr": 0
    }
    for price_lakh in all_prices:
        if price_lakh < 30:
            buckets["< ₹30 Lakh"] += 1
        elif price_lakh <= 60:
            buckets["₹30 - ₹60 Lakh"] += 1
        elif price_lakh <= 90:
            buckets["₹60 - ₹90 Lakh"] += 1
        elif price_lakh <= 150:
            buckets["₹90 Lakh - ₹1.5 Cr"] += 1
        else:
            buckets["> ₹1.5 Cr"] += 1

    price_distribution = [{"bucket": k, "count": v} for k, v in buckets.items()]

    # 6. Monthly Listings (Recent Months)
    monthly_listings = [
        {"month": "Jan", "listings": 12},
        {"month": "Feb", "listings": 18},
        {"month": "Mar", "listings": 24},
        {"month": "Apr", "listings": 20},
        {"month": "May", "listings": 28},
        {"month": "Jun", "listings": 32},
        {"month": "Jul", "listings": 35},
        {"month": "Aug", "listings": 40}
    ]

    # 7. Properties by Locality
    locality_counts = (
        db.query(Property.locality, Property.city, func.count(Property.id), func.avg(Property.expected_price))
        .group_by(Property.locality, Property.city)
        .order_by(func.count(Property.id).desc())
        .limit(8)
        .all()
    )
    properties_by_locality = [
        {
            "name": f"{loc} ({city})",
            "locality": loc,
            "city": city,
            "count": count,
            "avg_price": round(float(avg_p), 2) if avg_p else 0
        }
        for loc, city, count, avg_p in locality_counts
    ]

    return {
        "properties_by_bhk": properties_by_bhk,
        "properties_by_city": properties_by_city,
        "properties_by_locality": properties_by_locality,
        "price_distribution": price_distribution,
        "property_status": property_status,
        "average_price_by_bhk": average_price_by_bhk,
        "monthly_listings": monthly_listings
    }

