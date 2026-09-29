@echo off
echo ============================================================
echo  SmartHouse AI - Automated Setup Script for Windows
echo ============================================================
echo.

echo [1/5] Setting up Python virtual environment for Backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat

echo [2/5] Installing Backend dependencies...
pip install -r requirements.txt

echo [3/5] Generating synthetic housing dataset & training ML model...
python -m app.ml.train_model

echo [4/5] Seeding SQLite database with sample properties & clients...
python -m app.seed_data
cd ..

echo.
echo [5/5] Installing Frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ============================================================
echo  Setup Completed Successfully!
echo  Run 'run_project.bat' to launch the application.
echo ============================================================
pause
