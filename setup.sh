#!/bin/bash

echo "🚀 Setting up the environment..."

# Step 1: Create a virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📁 Creating virtual environment..."
    python3 -m venv venv
fi

# Step 2: Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate || source venv/Scripts/activate.bat || source venv/Scripts/activate.ps1

# Step 3: Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Step 4: Start the Flask server
echo "🚀 Starting the Flask server..."
python run.py
