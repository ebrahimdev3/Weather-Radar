# Advanced Weather Radar Dashboard

An interactive, high-contrast weather radar application built with a Python **FastAPI** backend and a **Leaflet.js** mobile-optimized frontend. The system provides real-time atmospheric visual layers over high-resolution satellite imagery with distinct airflow, thermal contours, and storm tracks.

## Key Features
- **True Terrain Satellite Base**: Powered by Google Satellite tiles to show detailed topography, mountains, and valleys on zoom.
- **High-Contrast Atmospheric Tracks**: Enhanced visual filters to clearly delineate thermal contours, precipitation radar cells, and airflow circulation vectors.
- **Dynamic Time Loop**: Fluid animation loop imitating active radar sweep and stream refreshes.
- **Adaptive UI Control**: Off-canvas sidebar configuration panel with responsive top-bar searching.
- **Geolocated Syncing**: On-click map coordinates targeting to fetch and display immediate sync data.

## 🛠️ Tech Stack & Dependencies
- **Backend**: Python 3.11+, FastAPI, Uvicorn, Requests
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism), Leaflet.js v1.9.4

---

## Getting Started (Local Deployment)

### 1. Clone & Setup Environment
Ensure your environment is running Python 3.10 or higher.
```bash
# Navigate to project directory
cd weather-radar-dashboard

# Install requirements
pip install -r requirements.txt



2. Start Backend Server

​Run the FastAPI application via Uvicorn on localhost:
uvicorn Backend.main:app --host 127.0.0.1 --port 8000 --reload



3. Launch Frontend

​Open Frontend/index.html via any local server environment or directly through your mobile development file viewer (e.g., Acode/Termux local server or any terminal you like). Ensure the BACKEND_BASE_URL in app.js correctly points to your live Uvicorn address.
​📂 Project Directory Structure
├── Backend/
│   ├── main.py            # FastAPI Application routes & Tile Server
│   └── ...
├── Frontend/
│   ├── index.html         # Main dashboard layout
│   ├── style.css          # Glassmorphism & High-contrast FX styling
│   └── app.js             # Leaflet initialization & UI logic
├── requirements.txt       # Python environment packages
└── README.md              # Project documentation

requirements.txt
fastapi>=0.100.0
uvicorn>=0.22.0
requests>=2.31.0
pydantic>=2.0



or you can just visit the website 
