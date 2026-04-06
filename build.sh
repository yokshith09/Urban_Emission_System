#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Generating grid data..."
python src/grid.py

echo "Running scoring models..."
python src/scoring.py

echo "Getting live AQI data..."
python src/aqi.py

echo "Running predictions..."
python src/model.py

echo "Build process complete!"
