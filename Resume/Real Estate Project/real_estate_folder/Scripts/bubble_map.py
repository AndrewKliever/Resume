import pandas as pd
import os
import folium
from folium import FeatureGroup, LayerControl

# Setting paths
base_path = r"C:\Users\skylo\Project-3-Group-6-DataV\real_estate_folder"
data_path = os.path.join(base_path, "Data", "cleaned_redfin_data_with_coords.csv")
output_map_path_2 = os.path.join(base_path, "Maps", "interactive_bubble_map.html")

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

# Handle missing values
data['avg.list price'] = data['avg.list price'].fillna(data['avg.list price'].mean())
data['avg.price/sqft'] = data['avg.price/sqft'].fillna(data['avg.price/sqft'].mean())
data['avg.days on market'] = data['avg.days on market'].fillna(data['avg.days on market'].mean())

# Aggregate data
state_data = data.groupby('state', as_index=False).agg({
    'avg.list price': 'mean',
    'avg.price/sqft': 'mean',
    'avg.days on market': 'mean'
})

# Add coordinates for each state
state_data['lat'] = state_data['state'].map(lambda x: state_centers.get(x, [None, None])[0])
state_data['lng'] = state_data['state'].map(lambda x: state_centers.get(x, [None, None])[1])

# Drop rows without lat/lng
state_data = state_data.dropna(subset=['lat', 'lng'])

# Create the map
bubble_map = folium.Map(location=[37.0902, -95.7129], zoom_start=5)

metrics = {
    'avg.list price': ('blue', 100000),  # Blue circles for avg.list price
    'avg.price/sqft': ('red', 10),       # Red circles for avg.price/sqft
    'avg.days on market': ('green', 10)   # Green circles for avg.days on market
}

# Add FeatureGroup for each metric and its circles
for metric, (color, scale) in metrics.items():
    layer = FeatureGroup(name=metric)  # Create a separate layer for each metric
    for _, row in state_data.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lng']],
            radius=row[metric] / scale,  # Adjust the size of the bubble based on the metric
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            tooltip=f"{row['state']}: {metric} = {row[metric]:,.2f}",
            popup=f"<b>{row['state']}</b><br>{metric}: {row[metric]:,.2f}"
        ).add_to(layer)
    layer.add_to(bubble_map)

# Add LayerControl for dropdown menu
LayerControl().add_to(bubble_map)

# Save the map
os.makedirs(os.path.dirname(output_map_path_2), exist_ok=True)
bubble_map.save(output_map_path_2)
print(f"Bubble map created and saved as '{output_map_path_2}'")

