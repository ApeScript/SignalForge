#!/bin/bash

echo "==============================="
echo " SIGNALFORGE INSTALLER"
echo "==============================="

echo "Step 1: Check Python version..."

python3 --version || { echo "Python3 not found. Please install Python 3.x"; exit 1; }

echo "Step 2: Create virtual environment..."
python3 -m venv venv

echo "Step 3: Activate virtual environment..."
source venv/bin/activate

echo "Step 4: Upgrade pip..."
pip install --upgrade pip

echo "Step 5: Install required packages..."
pip install -r requirements.txt

echo "Step 6: Create database if not exists..."
if [ ! -f "signalforge.db" ]; then
    echo "Creating SQLite Database..."
    python3 -c "from db.database import Database; Database()"
else
    echo "Database already exists."
fi

echo "Step 7: Create folders..."
mkdir -p logs
mkdir -p signals
mkdir -p reports

echo "==============================="
echo " Setup complete!"
echo "==============================="

echo ""
echo "To start CLI:"
echo "source venv/bin/activate && python3 run.py scan --wallet 0xabc..."
echo ""
echo "To start API:"
echo "source venv/bin/activate && python3 run.py"
echo ""
