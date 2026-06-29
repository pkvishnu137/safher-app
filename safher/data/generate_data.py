import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

cities = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873),
    "Ahmedabad": (23.0225, 72.5714),
    "Goa": (15.2993, 74.1240),
    "Bhopal": (23.2599, 77.4126),
    "Kochi": (9.9312, 76.2673),
}

languages = {
    "Mumbai": ["Hindi", "Marathi", "English", "Gujarati"],
    "Delhi": ["Hindi", "English", "Punjabi", "Urdu"],
    "Bangalore": ["Kannada", "English", "Hindi", "Tamil"],
    "Chennai": ["Tamil", "English", "Telugu", "Malayalam"],
    "Kolkata": ["Bengali", "Hindi", "English"],
    "Hyderabad": ["Telugu", "Hindi", "English", "Urdu"],
    "Pune": ["Marathi", "Hindi", "English"],
    "Jaipur": ["Hindi", "Rajasthani", "English"],
    "Ahmedabad": ["Gujarati", "Hindi", "English"],
    "Goa": ["Konkani", "English", "Hindi", "Portuguese"],
    "Bhopal": ["Hindi", "English", "Urdu"],
    "Kochi": ["Malayalam", "English", "Tamil", "Hindi"],
}

guardian_types = ["Verified Local Woman", "Host Family", "Certified Ally", "NGO Partner", "Hostel Guardian"]
specializations = ["Emergency Response", "Medical Help", "Escort Service", "Language Assist", "Legal Aid", "General Safety"]

first_names = ["Priya","Ananya","Riya","Neha","Kavya","Sneha","Pooja","Meera","Divya","Aisha",
               "Fatima","Sunita","Rekha","Geeta","Lakshmi","Sana","Nisha","Deepa","Radha","Asha",
               "Ramesh","Suresh","Arjun","Vikram","Sanjay","Mohan","Raj","Dev","Anil","Vinod"]
last_names = ["Sharma","Verma","Patel","Singh","Kumar","Reddy","Nair","Menon","Iyer","Joshi",
              "Gupta","Mehta","Shah","Das","Roy","Khan","Ali","Pillai","Rao","Mishra"]

guardians = []
for i in range(500):
    city = random.choice(list(cities.keys()))
    lat, lon = cities[city]
    lat += np.random.uniform(-0.05, 0.05)
    lon += np.random.uniform(-0.05, 0.05)
    lang_list = random.sample(languages[city], k=random.randint(1, min(3, len(languages[city]))))
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    guardians.append({
        "guardian_id": f"G{i+1:04d}",
        "name": name,
        "city": city,
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
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

df_guardians = pd.DataFrame(guardians)
df_guardians.to_csv("/home/claude/safher/data/guardians.csv", index=False)

# SOS incidents dataset
incidents = []
for i in range(200):
    city = random.choice(list(cities.keys()))
    lat, lon = cities[city]
    lat += np.random.uniform(-0.05, 0.05)
    lon += np.random.uniform(-0.05, 0.05)
    incidents.append({
        "incident_id": f"INC{i+1:04d}",
        "city": city,
        "type": random.choice(["Harassment", "Lost", "Medical", "Theft", "Unsafe Area", "Emergency"]),
        "resolved": random.choices([True, False], weights=[92, 8])[0],
        "response_time_min": random.randint(2, 25),
        "guardian_type_used": random.choice(guardian_types),
        "severity": random.choice(["Low", "Medium", "High"]),
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "year": random.randint(2021, 2024),
    })

pd.DataFrame(incidents).to_csv("/home/claude/safher/data/incidents.csv", index=False)

# Safety zones dataset
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
            "type": random.choice(["High Safety", "Moderate", "Caution", "Tourist Safe"]),
        })

pd.DataFrame(zones).to_csv("/home/claude/safher/data/safety_zones.csv", index=False)

print("✅ All datasets generated successfully!")
print(f"  Guardians: {len(guardians)}")
print(f"  Incidents: {len(incidents)}")
print(f"  Safety Zones: {len(zones)}")
