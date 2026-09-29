# AI House Price Predictor & Smart Property Management System ("SmartHouse AI")

> **Tagline:** Predict smarter. Price better. Find the right property.

A full-stack, enterprise-grade real estate platform combining Machine Learning price estimation, Smart BHK Comparison matrices, Property Inventory CRM, Client CRM, Best Deal Finder algorithms, CSV Exports, and a responsive React SaaS Dashboard.

---

## Key Features

1. **AI Property Price Predictor**
   - Estimates market property prices using a Scikit-Learn `Pipeline` (`RandomForestRegressor`).
   - Calculates **Fair Market Price**, **Best Deal Price**, **Negotiation Bounds**, **Price per Sq.Ft.**, and **Confidence Score**.
   - Provides valuation deal recommendations: *Below Estimated Market Value*, *Excellent Deal*, *Good Deal*, *Negotiation Recommended*, or *Potentially Overpriced*.
   - Includes a visual deal gauge meter and natural language AI explanation.

2. **Smart BHK Comparison Matrix**
   - Evaluates price escalation across 1 BHK, 2 BHK, 3 BHK, and 4 BHK configurations for any city or locality.
   - Shows target budget recommendations for property investors and buyers.

3. **Property Inventory Management**
   - Complete CRUD (Create, Read, Update, Delete) for property listings with automatic AI price estimation.
   - Search by Property ID, City, Locality, or Owner.
   - Filter by BHK, Property Type, Status (*Available*, *Under Negotiation*, *Sold*, *Rented*), and Price Range.
   - Sort by Price (Low/High) or Listing Date (Newest/Oldest).

4. **Client CRM**
   - Tracks prospective buyers, sellers, and renters.
   - Filters by budget, preferred city, requirement (*Buy*, *Rent*, *Sell*), and BHK preferences.
   - Validates contact phone numbers and email addresses.

5. **Best Deal Finder Algorithm**
   - Ranks active inventory properties based on discount percentage relative to AI valuation baseline.
   - Displays a custom **Deal Score (0 - 100)**.

6. **Interactive Analytics Dashboard**
   - Live KPI metric cards for active inventory, average property prices, and AI valuation tracking.
   - Visual charts powered by Recharts (Properties by BHK, City distributions, Price bands, Inventory status, Monthly listings trend).

7. **Data Exporter**
   - One-click CSV export downloads for both Property listings and Client records.

---

## Tech Stack

### Backend & Machine Learning
- **Python 3.11+**
- **FastAPI**: Modern, fast web framework for REST API endpoints
- **SQLAlchemy ORM & SQLite**: Relational database storage
- **Scikit-Learn**: Machine learning pipeline (`RandomForestRegressor`, `ColumnTransformer`, `OneHotEncoder`, `StandardScaler`)
- **Pandas & NumPy**: Data processing and synthetic housing dataset generation
- **Joblib**: Model serialization and persistence
- **Pydantic**: Request/response schema validation

### Frontend
- **React 18 & Vite**: Modern frontend library & fast dev environment
- **JavaScript (ES6+)**
- **Vanilla CSS**: CSS custom properties, Glassmorphism, Dark/Light theme mode
- **Recharts**: Interactive charting & data visualization library
- **Lucide React**: Clean SVG icon set
- **Axios**: HTTP API client

---

## Project Structure

```
house-price-predictor/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application & lifespan setup
│   │   ├── database.py          # SQLAlchemy SQLite connection & session
│   │   ├── models.py            # SQLAlchemy ORM models (Client, Property, Prediction)
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── crud.py              # Database query functions
│   │   ├── config.py            # Environment configuration
│   │   ├── seed_data.py         # Seed script for properties and clients
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── prediction.py    # ML prediction & BHK comparison APIs
│   │   │   ├── properties.py    # Property inventory APIs & CSV export
│   │   │   ├── clients.py       # Client CRM APIs & CSV export
│   │   │   └── dashboard.py     # Aggregated stats & chart dataset APIs
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── generate_dataset.py # Synthetic housing dataset generator
│   │   │   ├── train_model.py   # Model pipeline training script
│   │   │   ├── predictor.py     # Model inference engine
│   │   │   └── model_utils.py   # Valuation calculations & deal logic
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py    # Input validation helpers
│   ├── data/                    # Generated housing_data.csv (3500 rows)
│   ├── models/                  # Stores house_price_model.joblib & metrics.json
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # Sidebar, Navbar, StatsCard, PriceMeter, Modal, Toast
│   │   ├── pages/               # Dashboard, Predictor, Properties, PropertyDetail, Clients, BHKComparison, Deals, Analytics, About
│   │   ├── services/            # Axios API service module
│   │   ├── App.jsx              # React Router setup & dark mode layout
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Custom CSS system
│   ├── package.json
│   └── vite.config.js
├── README.md
├── .gitignore
├── run_project.bat              # One-click Windows runner
└── setup.bat                    # One-click Windows dependency & model setup
```

---

## Getting Started (Windows Commands)

### Option A: One-Click Setup & Launch (Recommended)

1. Double-click `setup.bat` to install virtual environments, dependencies, generate the ML dataset, train the model, and seed the database.
2. Double-click `run_project.bat` to start both the FastAPI backend server and Vite React frontend server.

---

### Option B: Manual Command Execution

#### 1. Setup Backend
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.ml.train_model
python -m app.seed_data
uvicorn app.main:app --reload --port 8000
```

#### 2. Setup Frontend (Open a second terminal)
```cmd
cd frontend
npm install
npm run dev
```

---

## Application Access URLs

- **Frontend Web Application:** [http://localhost:5173](http://localhost:5173)
- **Backend API Root:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Example Prediction API

### Request (`POST /api/predict`)
```json
{
  "city": "Delhi",
  "locality": "Connaught Place",
  "property_type": "Apartment",
  "bhk": 3,
  "total_sqft": 1600,
  "bathrooms": 3,
  "balcony": 2,
  "floor": 4,
  "total_floors": 10,
  "parking": 1,
  "furnishing_status": "Semi-Furnished",
  "property_age": 3,
  "facing": "East",
  "availability": "Ready to Move"
}
```

### Response
```json
{
  "predicted_price": 17850000.0,
  "fair_price": 17493000.0,
  "best_price": 16793000.0,
  "minimum_reasonable_price": 15785000.0,
  "maximum_reasonable_price": 18543000.0,
  "price_per_sqft": 11156.25,
  "confidence_score": 90.9,
  "recommendation": "Good Deal",
  "message": "Property is reasonably priced within fair market valuation parameters."
}
```

---

## License & Credits
Built for Portfolio, Resume, and Final-Year Project demonstration purposes.
Developed by Google DeepMind Antigravity AI Pair Programmer.
