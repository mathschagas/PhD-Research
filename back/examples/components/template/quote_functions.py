import math
import hashlib
from flask import jsonify

# Function to generate fixed values with better distribution based on component ID
def generate_fixed_values(component_id, min_value, max_value):
    # Generate a SHA-256 hash of the component_id
    hash_value = hashlib.sha256(component_id.encode('utf-8')).hexdigest()
    # Convert a portion of the hash (first 8 characters) to an integer
    hash_int = int(hash_value[:8], 16)
    # Map the hash value to the desired range
    return min_value + (hash_int % (max_value - min_value))

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

# Quote calculation functions for different types of components
def quote_drone(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 40, 60)
    cost_per_km = generate_fixed_values(component_id, 7, 12)
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values(component_id, 1, 10)
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    
    return jsonify(
        status="OK",
        cbr={
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": generate_fixed_values(component_id, 0, 1),
            "secure_container": generate_fixed_values(component_id, 0, 1)
        }
    )

def quote_car(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 30, 80)
    cost_per_km = generate_fixed_values(component_id, 9, 15)
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values(component_id, 1, 10)
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    
    return jsonify(
        status="OK",
        cbr={
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": 1,  # Cars are always rain-safe
            "secure_container": generate_fixed_values(component_id, 0, 1)
        }
    )

def quote_motorcycle(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 40, 50)
    cost_per_km = generate_fixed_values(component_id, 6, 10)
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values(component_id, 1, 10)
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    
    return jsonify(
        status="OK",
        cbr={
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": generate_fixed_values(component_id, 0, 1),
            "secure_container": generate_fixed_values(component_id, 0, 1)
        }
    )

def quote_bicycle(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 15, 25)
    cost_per_km = generate_fixed_values(component_id, 2, 5)
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values(component_id, 1, 10)
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    
    return jsonify(
        status="OK",
        cbr={
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": generate_fixed_values(component_id, 0, 1),
            "secure_container": generate_fixed_values(component_id, 0, 1)
        }
    )

def quote_truck(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 30, 50)
    cost_per_km = generate_fixed_values(component_id, 20, 30)
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values(component_id, 1, 10)
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    
    return jsonify(
        status="OK",
        cbr={
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": 1,  # Trucks are always rain-safe
            "secure_container": 1  # Trucks always have a secure container
        }
    )

def quote_pedestrian(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 3, 5)
    cost_per_km = 0  # Pedestrians do not have cost per km
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values(component_id, 1, 10)
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = 20  # Fixed cost for pedestrians
    
    return jsonify(
        status="OK",
        cbr={
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": 0,  # Pedestrians are never rain-safe
            "secure_container": 0  # Pedestrians never have a secure container
        }
    )

def quote_scooter(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 25, 35)
    cost_per_km = generate_fixed_values(component_id, 5, 10)
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    distance_to_package = generate_fixed_values(component_id, 1, 10)
    time_hours = (distance + distance_to_package) / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    
    return jsonify(
        status="OK",
        cbr={
            "time_to_deliver": time_to_deliver,
            "price": price,
            "safe_to_rain": generate_fixed_values(component_id, 0, 1),
            "secure_container": generate_fixed_values(component_id, 0, 1)
        }
    )

# Dictionary to access quote functions based on the component type
quote_functions = {
    "drone": quote_drone,
    "car": quote_car,
    "motorcycle": quote_motorcycle,
    "bicycle": quote_bicycle,
    "truck": quote_truck,  # Trucks always have a secure container
    "pedestrian": quote_pedestrian,
    "scooter": quote_scooter,
}
