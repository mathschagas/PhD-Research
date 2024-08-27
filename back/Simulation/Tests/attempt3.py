import random
import requests
import math
import time

# Constants
MAX_DISTANCE_KM = 30  # Maximum distance a drone can travel in km
DRONE_SPEED_KMH = 60  # Average speed of drone in km/h (realistic for delivery drones)
EARTH_RADIUS_KM = 6371  # Radius of the Earth in km

# Function to calculate distance between two lat/lon coordinates using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c

# Function to get a random location within London
def get_random_location():
    # London bounding box coordinates
    lat_min, lat_max = 51.286760, 51.691874
    lon_min, lon_max = -0.5103751, 0.3340155
    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    return lat, lon

# Function to get address from coordinates using Nominatim
def get_address(lat, lon):
    response = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json")
    data = response.json()
    address = data.get('display_name', 'Unknown Address')
    return address

# Function to simulate the drone delivery process
def simulate_drone_delivery():
    # Get random pickup and drop-off points
    pickup_lat, pickup_lon = get_random_location()
    dropoff_lat, dropoff_lon = get_random_location()

    pickup_address = get_address(pickup_lat, pickup_lon)
    dropoff_address = get_address(dropoff_lat, dropoff_lon)

    print(f"Pickup Address: {pickup_address}")
    print(f"Dropoff Address: {dropoff_address}")

    total_distance = haversine(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
    distance_covered = 0.0

    print(f"Total Distance: {total_distance:.2f} km")
    print("Starting drone delivery simulation...\n")

    while distance_covered < total_distance:
        # Simulate drone movement
        move_distance = min(1, total_distance - distance_covered)  # Move 1 km per iteration or less if close to the destination
        distance_covered += move_distance
        time_to_arrival = (total_distance - distance_covered) / (DRONE_SPEED_KMH / 3600)  # Time in seconds

        print(f"Drone moved {move_distance:.2f} km")
        print(f"Distance covered: {distance_covered:.2f} km")
        print(f"Speed: {DRONE_SPEED_KMH:.2f} km/h")
        print(f"Estimated time to arrival: {time_to_arrival:.2f} seconds")
        print()

        time.sleep(1)  # Simulate time passing

    print("Drone has reached the destination!")

if __name__ == "__main__":
    simulate_drone_delivery()
