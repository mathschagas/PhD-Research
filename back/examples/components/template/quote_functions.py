import math
import hashlib
from flask import jsonify

# Função para gerar valores fixos baseados no ID do componente
def generate_fixed_values(component_id, min_value, max_value):
    hash_value = int(hashlib.sha256(component_id.encode('utf-8')).hexdigest(), 16)
    return min_value + (hash_value % (max_value - min_value))

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    lat1, lon1 = map(math.radians, [lat1, lon1])
    lat2, lon2 = map(math.radians, [lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def quote_drone(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 50, 70)
    cost_per_km = generate_fixed_values(component_id, 50, 100) / 100
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    time_hours = distance / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    return jsonify(status="OK", cbr={"time_to_deliver": time_to_deliver, "price": price})

def quote_car(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 40, 60)
    cost_per_km = generate_fixed_values(component_id, 80, 120) / 100
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    time_hours = distance / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    return jsonify(status="OK", cbr={"time_to_deliver": time_to_deliver, "price": price})

def quote_motorcycle(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 60, 80)
    cost_per_km = generate_fixed_values(component_id, 70, 100) / 100
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    time_hours = distance / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    return jsonify(status="OK", cbr={"time_to_deliver": time_to_deliver, "price": price})

def quote_bicycle(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 15, 25)
    cost_per_km = generate_fixed_values(component_id, 10, 30) / 100
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    time_hours = distance / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    return jsonify(status="OK", cbr={"time_to_deliver": time_to_deliver, "price": price})

def quote_truck(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 30, 50)
    cost_per_km = generate_fixed_values(component_id, 150, 250) / 100
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    time_hours = distance / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    return jsonify(status="OK", cbr={"time_to_deliver": time_to_deliver, "price": price})

def quote_pedestrian(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 3, 5)
    cost_per_km = 0  # Pedestrians do not have a cost per km
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    time_hours = distance / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = 0  # No cost for walking
    return jsonify(status="OK", cbr={"time_to_deliver": time_to_deliver, "price": price})

def quote_scooter(lat1, lon1, lat2, lon2, component_id):
    speed = generate_fixed_values(component_id, 25, 35)
    cost_per_km = generate_fixed_values(component_id, 50, 100) / 100
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    time_hours = distance / speed
    time_to_deliver = round(time_hours * 60, 2)
    price = round(distance * cost_per_km, 2)
    return jsonify(status="OK", cbr={"time_to_deliver": time_to_deliver, "price": price})

quote_functions = {
    "drone": quote_drone,
    "car": quote_car,
    "motorcycle": quote_motorcycle,
    "bicycle": quote_bicycle,
    "truck": quote_truck,
    "pedestrian": quote_pedestrian,
    "scooter": quote_scooter,
}

