import math
import hashlib
import json
from flask import jsonify

with open('examples/components/template/quote_data.json', 'r') as file:
    QUOTE_DATA = json.load(file)

# Function to generate fixed values with better distribution based on component ID
def generate_fixed_values(attribute, component_id, min_value, max_value):
    if min_value == max_value:
        return min_value
    # Generate a SHA-256 hash of the component_id
    attr_id = attribute + component_id
    hash_value = hashlib.sha256(attr_id.encode('utf-8')).hexdigest()
    # Convert the first 8 characters of the hash to an integer
    hash_int = int(hash_value[:8], 16)
    # Map the hash value to the desired range
    return min_value + (hash_int % (max_value - min_value + 1))

# Function to calculate the haversine distance between two latitude/longitude points
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    lat1, lon1 = map(math.radians, [lat1, lon1])
    lat2, lon2 = map(math.radians, [lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def quote(component_type, lat1, lon1, lat2, lon2, component_id):
    if component_type not in QUOTE_DATA:
        return jsonify(
            status="ERROR",
            message="Component type not found."
        )

    speed = generate_fixed_values("speed", component_id, QUOTE_DATA[component_type]['speed_min'], QUOTE_DATA[component_type]['speed_max'])
    cost_per_km = generate_fixed_values("cost_per_km", component_id, QUOTE_DATA[component_type]['cost_per_km_min'], QUOTE_DATA[component_type]['cost_per_km_max'])
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values("distance_to_package", component_id, QUOTE_DATA[component_type]['distance_to_package_min'], QUOTE_DATA[component_type]['distance_to_package_max'])
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    if component_type == "pedestrian":
        price = 20

    return jsonify(
        status="OK",
        cbr={
            "distance_to_package": distance_to_package,
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": generate_fixed_values("safe_to_rain", component_id, QUOTE_DATA[component_type]['safe_to_rain_min'], QUOTE_DATA[component_type]['safe_to_rain_max']),
            "secure_container": generate_fixed_values("secure_container", component_id, QUOTE_DATA[component_type]['secure_container_min'], QUOTE_DATA[component_type]['secure_container_max'])
        }
    )