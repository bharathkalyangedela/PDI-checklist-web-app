@echo off
echo 🚀 Setting up the environment...

if not exist venv (
    echo 📁 Creating virtual environment...
    python -m venv venv
)

echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🚀 Starting the Flask server...
python run.py

pause
