# Urban Emission Intelligence System (UEIS) – GHMC

A live, automated emission monitoring system for GHMC that:
- Calculates new hotspots
- Integrates real-time AQI
- Predicts next 24-hour pollution
- Validates using satellite data
- Runs as a public dashboard

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate base grids and scores:
   ```bash
   python src/grid.py
   python src/scoring.py
   ```
3. Fetch Live AQI:
   ```bash
   python src/aqi.py
   ```
4. Run forecasting:
   ```bash
   python src/model.py
   ```
5. Launch the Dashboard:
   ```bash
   streamlit run app/app.py
   ```
