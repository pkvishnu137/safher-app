import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from math import radians, cos, sin, asin, sqrt
import time
import random
import os

# ─── Inline Data Generation (no CSV files needed) ────────────────────────────
def generate_all_data():
    random.seed(42)
    np.random.seed(42)

    cities = {
        "Mumbai": (19.0760, 72.8777), "Delhi": (28.6139, 77.2090),
        "Bangalore": (12.9716, 77.5946), "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639), "Hyderabad": (17.3850, 78.4867),
        "Pune": (18.5204, 73.8567), "Jaipur": (26.9124, 75.7873),
        "Ahmedabad": (23.0225, 72.5714), "Goa": (15.2993, 74.1240),
        "Bhopal": (23.2599, 77.4126), "Kochi": (9.9312, 76.2673),
    }
    languages = {
        "Mumbai": ["Hindi","Marathi","English","Gujarati"],
        "Delhi": ["Hindi","English","Punjabi","Urdu"],
        "Bangalore": ["Kannada","English","Hindi","Tamil"],
        "Chennai": ["Tamil","English","Telugu","Malayalam"],
        "Kolkata": ["Bengali","Hindi","English"],
        "Hyderabad": ["Telugu","Hindi","English","Urdu"],
        "Pune": ["Marathi","Hindi","English"],
        "Jaipur": ["Hindi","Rajasthani","English"],
        "Ahmedabad": ["Gujarati","Hindi","English"],
        "Goa": ["Konkani","English","Hindi"],
        "Bhopal": ["Hindi","English","Urdu"],
        "Kochi": ["Malayalam","English","Tamil","Hindi"],
    }
    guardian_types = ["Verified Local Woman","Host Family","Certified Ally","NGO Partner","Hostel Guardian"]
    specializations = ["Emergency Response","Medical Help","Escort Service","Language Assist","Legal Aid","General Safety"]
    first_names = ["Priya","Ananya","Riya","Neha","Kavya","Sneha","Pooja","Meera","Divya","Aisha",
                   "Fatima","Sunita","Rekha","Geeta","Lakshmi","Sana","Nisha","Deepa","Radha","Asha",
                   "Ramesh","Suresh","Arjun","Vikram","Sanjay","Mohan","Raj","Dev","Anil","Vinod"]
    last_names = ["Sharma","Verma","Patel","Singh","Kumar","Reddy","Nair","Menon","Iyer","Joshi",
                  "Gupta","Mehta","Shah","Das","Roy","Khan","Ali","Pillai","Rao","Mishra"]

    guardians = []
    for i in range(500):
        city = random.choice(list(cities.keys()))
        lat, lon = cities[city]
        lang_list = random.sample(languages[city], k=random.randint(1, min(3, len(languages[city]))))
        guardians.append({
            "guardian_id": f"G{i+1:04d}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "city": city,
            "latitude": round(lat + np.random.uniform(-0.05, 0.05), 6),
            "longitude": round(lon + np.random.uniform(-0.05, 0.05), 6),
            "type": random.choice(guardian_types),
            "specialization": random.choice(specializations),
            "languages": ", ".join(lang_list),
            "rating": round(np.random.uniform(3.8, 5.0), 1),
            "response_time_min": random.randint(3, 20),
            "verified": random.choices([True, False], weights=[85, 15])[0],
            "available_now": random.choices([True, False], weights=[60, 40])[0],
            "total_assists": random.randint(5, 300),
            "background_checked": random.choices([True, False], weights=[90, 10])[0],
            "phone": f"+91 {random.randint(7000000000, 9999999999)}",
            "joined_year": random.randint(2020, 2024),
        })

    incidents = []
    for i in range(200):
        city = random.choice(list(cities.keys()))
        lat, lon = cities[city]
        incidents.append({
            "incident_id": f"INC{i+1:04d}",
            "city": city,
            "type": random.choice(["Harassment","Lost","Medical","Theft","Unsafe Area","Emergency"]),
            "resolved": random.choices([True, False], weights=[92, 8])[0],
            "response_time_min": random.randint(2, 25),
            "guardian_type_used": random.choice(guardian_types),
            "severity": random.choice(["Low","Medium","High"]),
            "latitude": round(lat + np.random.uniform(-0.05, 0.05), 6),
            "longitude": round(lon + np.random.uniform(-0.05, 0.05), 6),
            "year": random.randint(2021, 2024),
        })

    zones = []
    for city, (lat, lon) in cities.items():
        for j in range(random.randint(5, 12)):
            zones.append({
                "zone_id": f"Z{len(zones)+1:04d}",
                "city": city,
                "name": f"{city} Zone {j+1}",
                "latitude": round(lat + np.random.uniform(-0.08, 0.08), 6),
                "longitude": round(lon + np.random.uniform(-0.08, 0.08), 6),
                "safety_score": round(np.random.uniform(50, 99), 1),
                "guardian_count": random.randint(3, 25),
                "type": random.choice(["High Safety","Moderate","Caution","Tourist Safe"]),
            })

    return pd.DataFrame(guardians), pd.DataFrame(incidents), pd.DataFrame(zones)

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SafHer — Women's Travel Safety Network",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%);
    color: #f0e6ff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d1b4e 0%, #1a0a2e 100%);
    border-right: 1px solid rgba(196, 130, 255, 0.2);
}
[data-testid="stSidebar"] * { color: #e8d5ff !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label { color: #c482ff !important; font-size: 0.82rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }

/* Metric cards */
.metric-card {
    background: rgba(196, 130, 255, 0.08);
    border: 1px solid rgba(196, 130, 255, 0.25);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(196,130,255,0.18);
}
.metric-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #c482ff;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a07cd0;
    margin-top: 4px;
}

/* SOS Button */
.sos-container {
    display: flex;
    justify-content: center;
    margin: 12px 0;
}
.sos-btn {
    background: linear-gradient(135deg, #ff1744, #d50000);
    color: white !important;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    padding: 18px 60px;
    border-radius: 50px;
    border: none;
    cursor: pointer;
    box-shadow: 0 0 40px rgba(255,23,68,0.5);
    animation: pulse-sos 1.8s ease-in-out infinite;
    width: 100%;
    font-family: 'DM Sans', sans-serif;
}
@keyframes pulse-sos {
    0%, 100% { box-shadow: 0 0 40px rgba(255,23,68,0.5); }
    50% { box-shadow: 0 0 70px rgba(255,23,68,0.85); }
}

/* Guardian card */
.guardian-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(196,130,255,0.2);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    transition: all 0.2s;
}
.guardian-card:hover {
    background: rgba(196,130,255,0.1);
    border-color: rgba(196,130,255,0.5);
    transform: translateX(4px);
}
.guardian-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: #e8d5ff;
}
.guardian-badge {
    display: inline-block;
    background: rgba(196,130,255,0.15);
    border: 1px solid rgba(196,130,255,0.35);
    color: #c482ff;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-right: 6px;
    margin-top: 5px;
}
.badge-green {
    background: rgba(0,230,118,0.12);
    border-color: rgba(0,230,118,0.35);
    color: #00e676;
}
.badge-red {
    background: rgba(255,23,68,0.12);
    border-color: rgba(255,23,68,0.35);
    color: #ff1744;
}

/* Section headers */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    color: #e8d5ff;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 0.84rem;
    color: #a07cd0;
    margin-bottom: 20px;
    letter-spacing: 0.03em;
}

/* Hero */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    background: linear-gradient(135deg, #c482ff, #ff6b9d, #ffb347);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
}
.hero-sub {
    font-size: 1.05rem;
    color: #b09cc8;
    line-height: 1.7;
    max-width: 560px;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(196,130,255,0.06);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(196,130,255,0.15);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #a07cd0;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.87rem;
    letter-spacing: 0.04em;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7b2fbe, #c482ff) !important;
    color: white !important;
}

/* Inputs */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background: rgba(196,130,255,0.08) !important;
    border: 1px solid rgba(196,130,255,0.3) !important;
    color: #e8d5ff !important;
    border-radius: 10px !important;
}
.stSlider [data-testid="stSlider"] { accent-color: #c482ff; }

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7b2fbe, #c482ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 10px 24px !important;
}

/* Divider */
.divider { border-top: 1px solid rgba(196,130,255,0.15); margin: 24px 0; }

/* Alert box */
.alert-box {
    background: rgba(255,23,68,0.1);
    border: 1px solid rgba(255,23,68,0.35);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    color: #ff6b6b;
    font-weight: 500;
}
.success-box {
    background: rgba(0,230,118,0.08);
    border: 1px solid rgba(0,230,118,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    color: #00e676;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return generate_all_data()

guardians_df, incidents_df, zones_df = load_data()


# ─── Helper Functions ─────────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def stars(rating):
    full = int(rating)
    return "★" * full + "☆" * (5 - full) + f" {rating}"

CITY_COORDS = {
    "Mumbai": (19.0760, 72.8777), "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946), "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639), "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567), "Jaipur": (26.9124, 75.7873),
    "Ahmedabad": (23.0225, 72.5714), "Goa": (15.2993, 74.1240),
    "Bhopal": (23.2599, 77.4126), "Kochi": (9.9312, 76.2673),
}

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px;'>
        <div style='font-size:2.4rem;'>🛡️</div>
        <div style='font-family:"DM Serif Display",serif; font-size:1.6rem; color:#c482ff;'>SafHer</div>
        <div style='font-size:0.72rem; color:#7b5c9e; letter-spacing:0.12em; text-transform:uppercase;'>Women's Safety Network</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    selected_city = st.selectbox("📍 Your City", list(CITY_COORDS.keys()))
    radius_km = st.slider("Search Radius (km)", 1, 30, 10)

    st.markdown("---")
    st.markdown("**Filter Guardians**")
    guardian_type = st.selectbox("Guardian Type", ["All"] + list(guardians_df["type"].unique()))
    only_verified = st.checkbox("Verified Only ✓", value=True)
    only_available = st.checkbox("Available Now 🟢", value=False)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#5a3d7a; text-align:center; line-height:1.6;'>
    SafHer v1.0 · Built for safety<br>
    Every guardian is background-checked
    </div>
    """, unsafe_allow_html=True)

# ─── Main Tabs ────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏠 Home", "🛡️ Find Guardians", "🆘 SOS Center", "📊 Safety Map", "📈 Insights"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: HOME
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("""
        <div style='padding: 32px 0 16px;'>
            <div class='hero-title'>Travel Fearlessly.<br>We've Got Your Back.</div>
            <div style='margin-top:16px;' class='hero-sub'>
                SafHer connects solo women travelers with verified local guardians — 
                real people, background-checked and ready to help in minutes.
                No more feeling alone in an unfamiliar city.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        stats = [
            (len(guardians_df[guardians_df["verified"]]), "Verified Guardians"),
            (len(guardians_df["city"].unique()), "Cities Covered"),
            (f"{incidents_df['resolved'].mean()*100:.0f}%", "Resolution Rate"),
        ]
        for col, (num, label) in zip([col_a, col_b, col_c], stats):
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-num'>{num}</div>
                    <div class='metric-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        # City safety overview radar
        city_data = guardians_df[guardians_df["city"] == selected_city]
        avg_rating = city_data["rating"].mean() if len(city_data) > 0 else 0
        verified_count = city_data["verified"].sum()
        available_count = city_data["available_now"].sum()
        avg_response = city_data["response_time_min"].mean() if len(city_data) > 0 else 0

        fig = go.Figure()
        categories = ["Rating", "Verified\nGuardians", "Available\nNow", "Fast\nResponse", "Coverage"]
        values_raw = [avg_rating, verified_count, available_count, max(0, 20 - avg_response), len(city_data)]
        max_vals = [5, 100, 50, 20, 100]
        values = [min(v/m*5, 5) for v, m in zip(values_raw, max_vals)]

        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(196,130,255,0.18)',
            line=dict(color='#c482ff', width=2.5),
            name=selected_city,
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 5], gridcolor='rgba(196,130,255,0.15)',
                                tickfont=dict(color='#7b5c9e', size=9), tickvals=[1,2,3,4,5]),
                angularaxis=dict(tickfont=dict(color='#c482ff', size=11), gridcolor='rgba(196,130,255,0.12)'),
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text=f"Safety Profile — {selected_city}", font=dict(color='#e8d5ff', size=14), x=0.5),
            margin=dict(l=40, r=40, t=50, b=40),
            height=320,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-title'>How SafHer Works</div>
    <div class='section-sub'>Three steps to feeling safe anywhere</div>
    """, unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)
    how_it_works = [
        ("📍", "Set Your Location", "Tell us which city you're in. SafHer instantly maps verified guardians nearby."),
        ("🔍", "Browse Guardians", "Filter by type, language, and specialization. Every guardian is background-checked."),
        ("📞", "Connect Instantly", "Tap to call or message a guardian. Average response time: under 8 minutes."),
        ("🆘", "SOS Anytime", "Feeling threatened? Hit SOS and the nearest available guardian is alerted immediately."),
    ]
    for col, (icon, title, desc) in zip([h1, h2, h3, h4], how_it_works):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='text-align:left;'>
                <div style='font-size:1.8rem; margin-bottom:10px;'>{icon}</div>
                <div style='font-weight:700; color:#e8d5ff; font-size:0.95rem; margin-bottom:6px;'>{title}</div>
                <div style='font-size:0.82rem; color:#a07cd0; line-height:1.55;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: FIND GUARDIANS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown(f"""
    <div class='section-title'>Guardians in {selected_city}</div>
    <div class='section-sub'>Background-checked locals ready to help you</div>
    """, unsafe_allow_html=True)

    city_lat, city_lon = CITY_COORDS[selected_city]
    filtered = guardians_df[guardians_df["city"] == selected_city].copy()
    filtered["distance_km"] = filtered.apply(
        lambda r: haversine(city_lat, city_lon, r["latitude"], r["longitude"]), axis=1
    )
    filtered = filtered[filtered["distance_km"] <= radius_km]
    if only_verified:
        filtered = filtered[filtered["verified"] == True]
    if only_available:
        filtered = filtered[filtered["available_now"] == True]
    if guardian_type != "All":
        filtered = filtered[filtered["type"] == guardian_type]
    filtered = filtered.sort_values(["available_now", "rating"], ascending=[False, False])

    col_left, col_right = st.columns([1, 1.4])

    with col_left:
        st.markdown(f"**{len(filtered)} guardians found** within {radius_km} km")
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        if len(filtered) == 0:
            st.markdown("<div class='alert-box'>⚠️ No guardians found. Try increasing the search radius or adjusting filters.</div>", unsafe_allow_html=True)
        else:
            for _, row in filtered.head(8).iterrows():
                avail_badge = '<span class="guardian-badge badge-green">🟢 Available</span>' if row["available_now"] else '<span class="guardian-badge badge-red">🔴 Busy</span>'
                verified_badge = '<span class="guardian-badge">✓ Verified</span>' if row["verified"] else ''
                st.markdown(f"""
                <div class='guardian-card'>
                    <div class='guardian-name'>{row['name']}</div>
                    <div style='font-size:0.78rem; color:#7b5c9e; margin:3px 0 7px;'>
                        {row['type']} · {row['specialization']}
                    </div>
                    {avail_badge}{verified_badge}
                    <div style='margin-top:10px; font-size:0.8rem; color:#a07cd0; line-height:1.7;'>
                        ⭐ {stars(row['rating'])} &nbsp;|&nbsp; ⏱ {row['response_time_min']} min &nbsp;|&nbsp; 📍 {row['distance_km']:.1f} km<br>
                        🗣 {row['languages']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        map_data = filtered.copy()
        if len(map_data) > 0:
            fig_map = px.scatter_mapbox(
                map_data,
                lat="latitude", lon="longitude",
                color="available_now",
                color_discrete_map={True: "#00e676", False: "#ff1744"},
                size="rating",
                size_max=14,
                hover_name="name",
                hover_data={"type": True, "rating": True, "response_time_min": True,
                            "specialization": True, "available_now": True, "latitude": False, "longitude": False},
                zoom=11,
                height=500,
                labels={"available_now": "Available"},
            )
            fig_map.add_scattermapbox(
                lat=[city_lat], lon=[city_lon],
                mode="markers",
                marker=dict(size=18, color="#c482ff", symbol="star"),
                name="You",
                hovertext="📍 Your Location",
            )
            fig_map.update_layout(
                mapbox_style="carto-darkmatter",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(font=dict(color='#e8d5ff'), bgcolor='rgba(0,0,0,0.4)'),
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("No guardians to display on map.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: SOS CENTER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px;'>
        <div class='section-title'>🆘 SOS Center</div>
        <div class='section-sub'>Tap once. Help is on the way.</div>
    </div>
    """, unsafe_allow_html=True)

    col_sos, col_info = st.columns([1, 1.3])

    with col_sos:
        st.markdown("""
        <div style='background: rgba(255,23,68,0.07); border: 1px solid rgba(255,23,68,0.2);
             border-radius:18px; padding: 28px 24px; text-align:center; margin-bottom:16px;'>
            <div style='font-size:0.8rem; font-weight:700; letter-spacing:0.1em;
                 text-transform:uppercase; color:#ff6b6b; margin-bottom:8px;'>Emergency Mode</div>
            <div style='font-family:"DM Serif Display",serif; font-size:1.4rem;
                 color:#e8d5ff; line-height:1.4; margin-bottom:18px;'>
                Feeling unsafe or in danger?<br>Activate SOS now.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if "sos_active" not in st.session_state:
            st.session_state.sos_active = False
        if "sos_guardian" not in st.session_state:
            st.session_state.sos_guardian = None

        if st.button("🆘  ACTIVATE SOS", use_container_width=True):
            st.session_state.sos_active = True
            avail = guardians_df[
                (guardians_df["city"] == selected_city) & (guardians_df["available_now"] == True)
            ]
            if len(avail) > 0:
                st.session_state.sos_guardian = avail.sort_values("response_time_min").iloc[0]

        if st.session_state.sos_active and st.session_state.sos_guardian is not None:
            g = st.session_state.sos_guardian
            st.markdown(f"""
            <div class='success-box'>
                ✅ <strong>SOS Activated!</strong><br><br>
                Guardian <strong>{g['name']}</strong> has been notified.<br>
                Type: {g['type']}<br>
                ETA: <strong>~{g['response_time_min']} minutes</strong><br>
                Contact: {g['phone']}<br><br>
                Stay where you are. Help is coming. 💜
            </div>
            """, unsafe_allow_html=True)
            if st.button("Cancel SOS"):
                st.session_state.sos_active = False
                st.session_state.sos_guardian = None
                st.rerun()
        elif st.session_state.sos_active:
            st.markdown("<div class='alert-box'>⚠️ No available guardians found in your area right now. Calling emergency services recommended.</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='metric-card' style='text-align:left;'>
            <div style='font-weight:700; color:#c482ff; margin-bottom:10px;'>📋 SOS Checklist</div>
            <div style='font-size:0.85rem; color:#b09cc8; line-height:2;'>
            ☑ Stay in a visible public area<br>
            ☑ Keep your phone charged and visible<br>
            ☑ Share your live location with a trusted contact<br>
            ☑ Note the nearest landmark<br>
            ☑ Don't walk towards isolated areas
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class='section-title' style='font-size:1.3rem;'>Emergency Contacts</div>
        <div class='section-sub'>India-wide helplines</div>
        """, unsafe_allow_html=True)

        contacts = [
            ("🚨", "Women's Helpline", "1091"),
            ("🚔", "Police", "100"),
            ("🚑", "Ambulance", "108"),
            ("📞", "National Emergency", "112"),
            ("💜", "iCall (Mental Health)", "9152987821"),
            ("🛡️", "Cyber Crime Helpline", "1930"),
        ]
        for icon, name, number in contacts:
            st.markdown(f"""
            <div style='display:flex; align-items:center; justify-content:space-between;
                 background:rgba(196,130,255,0.06); border:1px solid rgba(196,130,255,0.15);
                 border-radius:12px; padding:14px 18px; margin-bottom:10px;'>
                <div>
                    <span style='font-size:1.1rem;'>{icon}</span>
                    <span style='color:#e8d5ff; font-weight:600; margin-left:10px;'>{name}</span>
                </div>
                <div style='font-family:"DM Serif Display",serif; font-size:1.3rem; color:#c482ff;'>
                    {number}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        # Incident type distribution
        city_inc = incidents_df[incidents_df["city"] == selected_city]
        if len(city_inc) > 0:
            inc_counts = city_inc["type"].value_counts().reset_index()
            inc_counts.columns = ["type", "count"]
            fig_inc = px.bar(
                inc_counts, x="count", y="type", orientation="h",
                color="count", color_continuous_scale=["#7b2fbe", "#c482ff", "#ff6b9d"],
                title=f"Incident Types Reported — {selected_city}",
                labels={"count": "Reports", "type": "Incident"},
                height=240,
            )
            fig_inc.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(color='#e8d5ff', size=13),
                font=dict(color='#a07cd0'), coloraxis_showscale=False,
                margin=dict(l=0, r=0, t=40, b=0), yaxis=dict(gridcolor='rgba(196,130,255,0.08)'),
                xaxis=dict(gridcolor='rgba(196,130,255,0.08)'),
            )
            st.plotly_chart(fig_inc, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: SAFETY MAP
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown(f"""
    <div class='section-title'>Safety Zone Map — {selected_city}</div>
    <div class='section-sub'>Color-coded safety scores across city zones</div>
    """, unsafe_allow_html=True)

    city_zones = zones_df[zones_df["city"] == selected_city]
    city_lat, city_lon = CITY_COORDS[selected_city]

    col_m1, col_m2 = st.columns([2, 1])

    with col_m1:
        if len(city_zones) > 0:
            fig_zones = px.scatter_mapbox(
                city_zones,
                lat="latitude", lon="longitude",
                color="safety_score",
                color_continuous_scale=["#ff1744", "#ffb300", "#00e676"],
                size="guardian_count",
                size_max=20,
                hover_name="name",
                hover_data={"safety_score": True, "guardian_count": True, "type": True,
                            "latitude": False, "longitude": False},
                zoom=10, height=480,
                labels={"safety_score": "Safety Score"},
            )
            fig_zones.add_scattermapbox(
                lat=[city_lat], lon=[city_lon],
                mode="markers",
                marker=dict(size=20, color="#c482ff", symbol="star"),
                name="📍 You",
            )
            fig_zones.update_layout(
                mapbox_style="carto-darkmatter",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0),
                coloraxis_colorbar=dict(
                    title="Safety", tickfont=dict(color='#a07cd0'),
                    bgcolor='rgba(26,10,46,0.8)',
                    bordercolor='rgba(196,130,255,0.2)',
                    title_font=dict(color='#c482ff'),
                ),
            )
            st.plotly_chart(fig_zones, use_container_width=True)

    with col_m2:
        st.markdown("""
        <div class='metric-card' style='margin-bottom:16px;'>
            <div style='font-weight:700; color:#c482ff; margin-bottom:12px; font-size:0.85rem;
                 letter-spacing:0.06em; text-transform:uppercase;'>Safety Legend</div>
            <div style='font-size:0.83rem; line-height:2.2; color:#b09cc8;'>
                🟢 <strong style='color:#00e676;'>80–100</strong> — Very Safe<br>
                🟡 <strong style='color:#ffb300;'>60–79</strong> — Moderate<br>
                🔴 <strong style='color:#ff1744;'>Below 60</strong> — Use Caution
            </div>
        </div>
        """, unsafe_allow_html=True)

        if len(city_zones) > 0:
            high_safety = city_zones[city_zones["safety_score"] >= 80]
            mod_safety = city_zones[(city_zones["safety_score"] >= 60) & (city_zones["safety_score"] < 80)]
            low_safety = city_zones[city_zones["safety_score"] < 60]

            for count, label, color in [
                (len(high_safety), "High Safety Zones", "#00e676"),
                (len(mod_safety), "Moderate Zones", "#ffb300"),
                (len(low_safety), "Caution Zones", "#ff1744"),
            ]:
                st.markdown(f"""
                <div class='metric-card' style='margin-bottom:10px;'>
                    <div class='metric-num' style='color:{color};'>{count}</div>
                    <div class='metric-label'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            top_zones = city_zones.sort_values("safety_score", ascending=False).head(5)
            st.markdown("**🏆 Safest Areas**")
            for _, z in top_zones.iterrows():
                score_color = "#00e676" if z["safety_score"] >= 80 else "#ffb300"
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center;
                     padding:8px 0; border-bottom:1px solid rgba(196,130,255,0.1);'>
                    <span style='font-size:0.82rem; color:#b09cc8;'>{z['name']}</span>
                    <span style='font-weight:700; color:{score_color}; font-size:0.88rem;'>{z['safety_score']}</span>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""
    <div class='section-title'>Network Insights</div>
    <div class='section-sub'>How SafHer is making travel safer, city by city</div>
    """, unsafe_allow_html=True)

    # City comparison bar
    city_stats = guardians_df.groupby("city").agg(
        guardians=("guardian_id", "count"),
        avg_rating=("rating", "mean"),
        verified=("verified", "sum"),
        avg_response=("response_time_min", "mean"),
    ).reset_index()

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        fig1 = px.bar(
            city_stats.sort_values("guardians", ascending=True),
            x="guardians", y="city", orientation="h",
            color="avg_rating",
            color_continuous_scale=["#7b2fbe", "#c482ff", "#ff6b9d"],
            title="Guardians per City",
            labels={"guardians": "Total Guardians", "city": "", "avg_rating": "Avg Rating"},
            height=350,
        )
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(color='#e8d5ff', size=13),
            font=dict(color='#a07cd0'),
            xaxis=dict(gridcolor='rgba(196,130,255,0.08)'),
            yaxis=dict(gridcolor='rgba(196,130,255,0.08)'),
            coloraxis_colorbar=dict(tickfont=dict(color='#a07cd0'), bgcolor='rgba(0,0,0,0)',
                                    title_font=dict(color='#c482ff')),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_i2:
        g_types = guardians_df["type"].value_counts().reset_index()
        g_types.columns = ["type", "count"]
        fig2 = px.pie(
            g_types, names="type", values="count",
            title="Guardian Types Distribution",
            color_discrete_sequence=["#c482ff", "#ff6b9d", "#7b2fbe", "#ffb347", "#00c9a7"],
            hole=0.45,
            height=350,
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(color='#e8d5ff', size=13),
            font=dict(color='#a07cd0'),
            legend=dict(font=dict(color='#b09cc8'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig2, use_container_width=True)

    col_i3, col_i4 = st.columns(2)

    with col_i3:
        inc_city = incidents_df.groupby("city")["resolved"].mean().reset_index()
        inc_city.columns = ["city", "resolution_rate"]
        inc_city["resolution_rate"] = (inc_city["resolution_rate"] * 100).round(1)
        fig3 = px.bar(
            inc_city.sort_values("resolution_rate"),
            x="city", y="resolution_rate",
            color="resolution_rate",
            color_continuous_scale=["#7b2fbe", "#c482ff", "#00e676"],
            title="Incident Resolution Rate by City (%)",
            labels={"resolution_rate": "Resolution %", "city": ""},
            height=320,
        )
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(color='#e8d5ff', size=13),
            font=dict(color='#a07cd0'),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor='rgba(196,130,255,0.08)', tickangle=35),
            yaxis=dict(gridcolor='rgba(196,130,255,0.08)'),
            margin=dict(l=0, r=0, t=40, b=60),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_i4:
        sev_counts = incidents_df["severity"].value_counts().reset_index()
        sev_counts.columns = ["severity", "count"]
        fig4 = px.funnel(
            sev_counts, x="count", y="severity",
            title="Incidents by Severity Level",
            color_discrete_sequence=["#ff1744", "#ffb300", "#00e676"],
            height=320,
        )
        fig4.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(color='#e8d5ff', size=13),
            font=dict(color='#a07cd0'),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Summary stats row
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    s1, s2, s3, s4, s5 = st.columns(5)
    summary = [
        (len(guardians_df), "Total Guardians"),
        (f"{guardians_df['rating'].mean():.2f} ★", "Avg Rating"),
        (f"{guardians_df['response_time_min'].mean():.1f} min", "Avg Response"),
        (f"{incidents_df['resolved'].mean()*100:.0f}%", "Cases Resolved"),
        (len(zones_df), "Safety Zones"),
    ]
    for col, (num, label) in zip([s1, s2, s3, s4, s5], summary):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-num'>{num}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)