# 🏙️ Urban Emission Intelligence System (UEIS) – GHMC

[![CI/CD Status](https://github.com/yokshith09/Urban_Emission_Project/actions/workflows/ci.yml/badge.svg)](https://github.com/yokshith09/Urban_Emission_Project/actions)

A fully automated, real-time emission and atmospheric monitoring system specifically designed for the **Greater Hyderabad Municipal Corporation (GHMC)**. 

UEIS dynamically synthesizes localized traffic density, industrial scores, live weather payloads, and real-time PM2.5 metrics into a high-performance **Streamlit Dashboard** armed with an AI-driven insights engine.

## 🌟 Key Features
* **🤖 AI Analyst Engine**: Continuously scans the region and updates localized textual warnings for maximum critical PM2.5 hotspots and traffic drivers. 
* **🔄 Live 60-Second Auto-Refresh**: Seamless, non-disruptive automated background metric synchronization.
* **🌥️ Real-Time Atmospheric Popups**: Live interactive floating Toasts alerting viewers of immediate grid changes in Temperature, Humidity, Wind Speed, and Air Quality Indexes, built upon **Open-Meteo APIs**.
* **🔮 24-Hour Horizon Forecasting**: Utilizes a customized Time-Series **FB Prophet** model tracking daily PM2.5 trends targeting 9 AM and 6 PM congestion peaks.
* **🛰️ Satellite Validation**: Overlay support for Google Earth Engine Sentinel-5P NO2 geospatial footprints.
* **🌐 Dynamic Date Scaling**: Intelligently variance scales API tracking structures so viewers can transparently traverse historical weekend drops and workday traffic-spikes.

## 🛠️ Tech Stack
* **Frontend**: Streamlit, Streamlit-Folium, Plotly Express
* **Backend Processing**: Pandas, GeoPandas, Numpy
* **Machine Learning & Time-Series**: FB Prophet
* **Automation & DevOps**: GitHub Actions CI/CD Pipeline

---

## 🚀 Local Setup & Deployment

### 1. Install Requirements
Create a virtual environment (optional) and install all package constraints:
```bash
pip install -r requirements.txt
```

### 2. Generate GeoSpatial Foundation
Calculate standard grids and structural risk scores (this prepares localized boundaries):
```bash
python src/grid.py
python src/scoring.py
```

### 3. Fetch Live Air Quality Vectors
Poll API endpoints for foundational PM2.5 metrics across nodes:
```bash
python src/aqi.py
```

### 4. Build Predictive Models
Run the machine learning compiler to output 24-hr Prophet forecasts:
```bash
python src/model.py
```

### 5. Launch the Intelligence Dashboard
Spin up your local Streamlit instance (runs aggressively inside your localhost):
```bash
streamlit run app/app.py
```

---

## 📖 System Transparency
Every data variable is logged securely underneath an accessible `User Guide & Legend` tab inside the dashboard. This defines standard safety thresholds for PM2.5 indices, explains our normalized Traffic & Industrial 0.0 - 1.0 scaling system, and openly documents the internal AI calculation structure so the viewer retains complete trust in the data stream.
