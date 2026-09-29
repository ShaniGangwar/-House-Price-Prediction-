@echo off
echo ============================================================
echo  Starting AI House Price Predictor & Smart Property Management System
echo ============================================================
echo.

echo Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "SmartHouse AI Backend" cmd /k "cd backend && venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

timeout /t 4 /nobreak >nul

echo Starting Vite React Frontend on http://localhost:5173 ...
start "SmartHouse AI Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo  Backend Server: http://127.0.0.1:8000
echo  Swagger API Docs: http://127.0.0.1:8000/docs
echo  Frontend Application: http://localhost:5173
echo ============================================================
echo.
pause
