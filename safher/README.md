# 🛡️ SafHer — Women's Travel Safety Network

> **A verified guardian network app that gives solo women travelers an immediate human safety net in any city they visit.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

---

## 🌟 What is SafHer?

SafHer is a women-first travel safety platform that connects solo female travelers with **verified local guardians** — background-checked residents, host families, and certified allies who can provide immediate help in emergencies.

### The Problem
Solo women travelers face safety concerns in unfamiliar cities — harassment, getting lost, or emergencies with no local support network.

### The Solution
A real-time guardian network with SOS activation, safety zone maps, and instant emergency contacts — all in one app.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Find Guardians** | Browse verified locals filtered by city, type, availability |
| 🆘 **SOS Center** | One-tap emergency alert to nearest available guardian |
| 🗺️ **Safety Map** | Color-coded safety zone scores across city areas |
| 📊 **Insights Dashboard** | Network stats, resolution rates, city comparisons |
| 📍 **12 Cities Covered** | Mumbai, Delhi, Bangalore, Chennai, Kolkata, Hyderabad + more |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Visualizations**: Plotly
- **Data**: Pandas, NumPy (synthetic dataset with 500 guardians, 200 incidents, 100+ safety zones)
- **Distance**: Haversine formula for real proximity calculations

---

## 📦 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/safher-app.git
cd safher-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate datasets
python data/generate_data.py

# 4. Run the app
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path**: `app.py`
5. Click **Deploy**

---

## 📁 Project Structure

```
safher-app/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── data/
│   ├── generate_data.py    # Dataset generation script
│   ├── guardians.csv       # 500 verified guardian profiles
│   ├── incidents.csv       # 200 incident records
│   └── safety_zones.csv    # 100+ city safety zones
└── README.md
```

---

## 📊 Dataset Overview

- **500 Guardians** across 12 Indian cities with ratings, response times, languages, specializations
- **200 Incident Records** with types, severity, resolution status
- **103 Safety Zones** with color-coded safety scores

---

## 💜 Built For

Solo women travelers and backpackers who deserve to explore the world fearlessly.

---

*Built with 💜 by Vishnu · Problem source: Fix My Itch*
