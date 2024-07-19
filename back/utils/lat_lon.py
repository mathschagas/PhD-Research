import random
import math

from utils.normalization import normalize_minimize

def generate_random_position_london():
    # Defining the boundaries of the city of London
    lat_min, lat_max = 51.28, 51.70
    lon_min, lon_max = -0.50, 0.10
    
    # Generating a random latitude and longitude within the boundaries
    latitude = random.uniform(lat_min, lat_max)
    longitude = random.uniform(lon_min, lon_max)
    
    return latitude, longitude

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    # Converting degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of the Earth in kilometers
    r = 6371.0
    
    # Distance in kilometers
    distance = r * c
    
    return distance

# def calculate_score(distances, transport_modes):
#     costs = []
#     times = []
    
#     for mode in transport_modes:
#         for distance in distances:
#             cost, time, _, _ = calculate_cost_time(distance, mode)
#             costs.append(cost)
#             times.append(time)

#     normalized_costs = normalize_minimize(costs)
#     normalized_times = normalize_minimize(times)

#     # Criterion weights: adjustable as needed
#     weight_cost = 0.5
#     weight_time = 0.5

#     scores = []
#     for i in range(len(transport_modes)):
#         score = weight_cost * normalized_costs[i] + weight_time * normalized_times[i]
#         scores.append(score)

#     return scores

# # Example usage
# lat1, lon1 = generate_random_position_london()
# lat2, lon2 = generate_random_position_london()
# distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)

# transport_modes = ['car', 'motorcycle', 'walking']
# scores = calculate_score([distance], transport_modes)

# for i, mode in enumerate(transport_modes):
#     cost, time, speed, cost_per_km = calculate_cost_time(distance, mode)
#     print(f"Transport mode: {mode.capitalize()}")
#     print(f"Distance: {distance:.2f} km")
#     print(f"Cost: ${cost:.2f}")
#     print(f"Time: {time:.2f} minutes")
#     print(f"Speed: {speed:.2f} km/h")
#     print(f"Cost per km: ${cost_per_km:.2f}")
#     print(f"Normalized score: {scores[i]:.2f}\n")
