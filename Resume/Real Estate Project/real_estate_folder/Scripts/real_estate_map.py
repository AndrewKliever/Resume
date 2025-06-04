import pandas as pd
import os
import folium
from folium.plugins import HeatMap
from folium import LayerControl

# Setting paths
base_path = os.getcwd()
data_path = os.path.join(base_path, "Data", "cleaned_redfin_data_with_coords.csv")
output_map_path = os.path.join(base_path, "Maps", "interactive_real_estate_map.html")

# Load the cleaned data
data = pd.read_csv(data_path)

state_centers = {
    "Alabama": [32.806671, -86.791130],
    "Alaska": [61.370716, -152.404419],
    "Arizona": [33.729759, -111.431221],
    "Arkansas": [34.969704, -92.373123],
    "California": [36.116203, -119.681564],
    "Colorado": [39.059811, -105.311104],
    "Connecticut": [41.597782, -72.755371],
    "Delaware": [39.318523, -75.507141],
    "Florida": [27.766279, -81.686783],
    "Georgia": [33.040619, -83.643074],
    "Hawaii": [21.094318, -157.498337],
    "Idaho": [44.240459, -114.478828],
    "Illinois": [40.349457, -88.986137],
    "Indiana": [39.849426, -86.258278],
    "Iowa": [42.011539, -93.210526],
    "Kansas": [38.526600, -96.726486],
    "Kentucky": [37.668140, -84.670067],
    "Louisiana": [31.169546, -91.867805],
    "Maine": [44.693947, -69.381927],
    "Maryland": [39.063946, -76.802101],
    "Massachusetts": [42.230171, -71.530106],
    "Michigan": [43.326618, -84.536095],
    "Minnesota": [45.694454, -93.900192],
    "Mississippi": [32.741646, -89.678696],
    "Missouri": [38.456085, -92.288368],
    "Montana": [46.921925, -110.454353],
    "Nebraska": [41.125370, -98.268082],
    "Nevada": [38.313515, -117.055374],
    "New Hampshire": [43.452492, -71.563896],
    "New Jersey": [40.298904, -74.521011],
    "New Mexico": [34.840515, -106.248482],
    "New York": [42.165726, -74.948051],
    "North Carolina": [35.630066, -79.806419],
    "North Dakota": [47.528912, -99.784012],
    "Ohio": [40.388783, -82.764915],
    "Oklahoma": [35.565342, -96.928917],
    "Oregon": [44.572021, -122.070938],
    "Pennsylvania": [40.590752, -77.209755],
    "Rhode Island": [41.680893, -71.511780],
    "South Carolina": [33.856892, -80.945007],
    "South Dakota": [44.299782, -99.438828],
    "Tennessee": [35.747845, -86.692345],
    "Texas": [31.054487, -97.563461],
    "Utah": [40.150032, -111.862434],
    "Vermont": [44.045876, -72.710686],
    "Virginia": [37.769337, -78.169968],
    "Washington": [47.400902, -121.490494],
    "West Virginia": [38.491226, -80.954456],
    "Wisconsin": [44.268543, -89.616508],
    "Wyoming": [42.755966, -107.302490]
}

# Debugging: State names in data
print("Unique states in data (before fixes):", data['state'].unique())

# Standardize state names to match GeoJSON format
data['state'] = data['state'].str.replace('-', ' ')

# Debugging: Compare state names with GeoJSON
print("Unique states after replacing dashes:", data['state'].unique())
geojson_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
    "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
    "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
print("GeoJSON states:", geojson_states)

# Fill missing data
data['avg.list price'] = data['avg.list price'].fillna(data['avg.list price'].mean())
data['avg.price/sqft'] = data['avg.price/sqft'].fillna(data['avg.price/sqft'].mean())
data['avg.days on market'] = data['avg.days on market'].fillna(data['avg.days on market'].mean())

# 1. Aggregate Data for Choropleth
state_data = data.groupby('state', as_index=False).agg({
    'avg.list price': 'mean',
    'avg.price/sqft': 'mean',
    'avg.days on market': 'mean'
})

# Map state centers to the aggregated data
state_data['lat'] = state_data['state'].map(lambda x: state_centers.get(x, [None, None])[0])
state_data['lng'] = state_data['state'].map(lambda x: state_centers.get(x, [None, None])[1])

# Debugging: States with missing lat/lng
missing_centers = state_data[state_data[['lat', 'lng']].isnull().any(axis=1)]
print("States with missing centers:\n", missing_centers)

# Drop rows without lat/lng
state_data = state_data.dropna(subset=['lat', 'lng'])

# Load GeoJSON for US states
geojson_path = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"

# Create a base map
base_map = folium.Map(location=[37.0902, -95.7129], zoom_start=5)

# Add Choropleth Layers
metrics = ['avg.list price', 'avg.price/sqft', 'avg.days on market']
colors = ['YlGnBu', 'OrRd', 'PuBu']
legends = ['Average List Price ($)', 'Average Price per Sqft ($)', 'Average Days on Market']

for metric, color, legend in zip(metrics, colors, legends):
    folium.Choropleth(
        geo_data=geojson_path,
        name=metric,
        data=state_data,
        columns=['state', metric],
        key_on='feature.properties.name',
        fill_color=color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend
    ).add_to(base_map)

# Add Heat Map
heat_data = data[['lat', 'lng', 'avg.list price']].dropna()
HeatMap(
    data=heat_data[['lat', 'lng', 'avg.list price']].values,
    radius=15,
    blur=10,
    max_zoom=1
).add_to(base_map)

# Add Layer Control
folium.LayerControl().add_to(base_map)

# Save the Combined Map
os.makedirs(os.path.dirname(output_map_path), exist_ok=True)
base_map.save(output_map_path)
print(f"Interactive map created and saved as '{output_map_path}'")
