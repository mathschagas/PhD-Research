import random
import time
import math
import requests

class Drone:
    def __init__(self, id, start_x, start_y):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.speed_kmh = 60.0  # Average speed in km/h
        self.total_distance = 0
        self.distance_traveled = 0
        self.start_time = time.time()

    def move_towards(self, target_x, target_y, time_interval):
        previous_x, previous_y = self.x, self.y

        # Calculate the distance to move in this iteration based on speed and time interval
        distance_to_move = (self.speed_kmh / 3600) * time_interval  # Convert speed to km/s and multiply by time interval

        # Calculate the direction vector towards the target
        distance_to_target = self.calculate_distance(self.x, self.y, target_x, target_y)
        ratio = distance_to_move / distance_to_target if distance_to_target != 0 else 0
        self.x += ratio * (target_x - self.x)
        self.y += ratio * (target_y - self.y)

        # Calculate distance moved in this iteration
        distance_moved = self.calculate_distance(previous_x, previous_y, self.x, self.y)
        self.distance_traveled += distance_moved

        elapsed_time = time.time() - self.start_time
        eta = self.estimated_time_to_arrival(target_x, target_y)

        print(f"Drone {self.id} moved to ({self.x:.6f}, {self.y:.6f})")
        print(f"Tempo de entrega até o momento: {elapsed_time:.2f} segundos")
        print(f"Tempo estimado para entrega: {eta:.2f} segundos")
        print(f"Distância percorrida até o momento: {self.distance_traveled:.6f} km")
        print(f"Distância até o destino: {distance_to_target:.6f} km")
        print(f"Distância do trajeto completo: {self.total_distance:.6f} km")
        print(f"Velocidade do drone: {self.speed_kmh:.2f} km/h")

    def calculate_distance(self, x1, y1, x2, y2):
        # Using the Haversine formula for a more accurate distance calculation
        R = 6371  # Radius of the Earth in km
        lat1, lon1 = math.radians(x1), math.radians(y1)
        lat2, lon2 = math.radians(x2), math.radians(y2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def estimated_time_to_arrival(self, target_x, target_y):
        remaining_distance = self.calculate_distance(self.x, self.y, target_x, target_y)
        if self.speed_kmh > 0:
            # Estimate time to arrival in hours and convert to seconds
            return (remaining_distance / self.speed_kmh) * 3600
        else:
            return float('inf')  # In case the drone isn't moving

class Observer:
    def __init__(self):
        self.conditions = {
            "bad_weather": False,
            "restricted_airspace": False,
            "sensor_failure": False
        }

    def detect_uncertainties(self):
        # Simulating the random detection of uncertainties
        self.conditions["bad_weather"] = random.random() < 0.2
        self.conditions["restricted_airspace"] = random.random() < 0.2
        self.conditions["sensor_failure"] = random.random() < 0.2

    def report(self, lat, lon):
        print("\nCurrent Conditions:")
        for condition, state in self.conditions.items():
            print(f"  {condition}: {'Yes' if state else 'No'}")
        if any(self.conditions.values()):
            address = get_address(lat, lon)
            print(f"Problema detectado em: {address} ({lat:.6f}, {lon:.6f})")
        print()

# Define the bounding box for London (approximate latitude and longitude)
LONDON_BOUNDING_BOX = {
    "min_lat": 51.28,  # Southernmost point
    "max_lat": 51.70,  # Northernmost point
    "min_lon": -0.52,  # Westernmost point
    "max_lon": 0.33    # Easternmost point
}

def random_position_within_london():
    lat = random.uniform(LONDON_BOUNDING_BOX["min_lat"], LONDON_BOUNDING_BOX["max_lat"])
    lon = random.uniform(LONDON_BOUNDING_BOX["min_lon"], LONDON_BOUNDING_BOX["max_lon"])
    return lat, lon

def get_address(lat, lon):
    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json")
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        address = data.get('display_name', 'Unknown Address')
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching address for ({lat}, {lon}): {e}")
        address = 'Unknown Address'
    return address

# Initial positions and target
start_x, start_y = random_position_within_london()
target_x, target_y = random_position_within_london()

# Create a drone and an observer
drone = Drone(id=1, start_x=start_x, start_y=start_y)
observer = Observer()

# Get addresses for logging
start_address = get_address(start_x, start_y)
target_address = get_address(target_x, target_y)

# Calculate the total distance from start to target
drone.total_distance = drone.calculate_distance(start_x, start_y, target_x, target_y)

print(f"Drone {drone.id} starting at ({drone.x:.6f}, {drone.y:.6f})")
print(f"Pickup Address: {start_address} ({start_x:.6f}, {start_y:.6f})")
print(f"Target Address: {target_address} ({target_x:.6f}, {target_y:.6f})")
print(f"Total distance to target: {drone.total_distance:.6f} km\n")

# Simulation loop with a configurable time interval
time_interval = 10  # seconds
log_interval = 1  # seconds

while (round(drone.x, 4), round(drone.y, 4)) != (round(target_x, 4), round(target_y, 4)):
    observer.detect_uncertainties()
    observer.report(drone.x, drone.y)

    if observer.conditions["bad_weather"]:
        print(f"Drone {drone.id} cannot proceed due to bad weather.")
    elif observer.conditions["restricted_airspace"]:
        print(f"Drone {drone.id} cannot proceed due to restricted airspace.")
    elif observer.conditions["sensor_failure"]:
        print(f"Drone {drone.id} experienced sensor failure.")
    else:
        drone.move_towards(target_x, target_y, time_interval)
        eta = drone.estimated_time_to_arrival(target_x, target_y)
        print(f"Estimated time to arrival: {eta:.2f} seconds")

    # Simulate time passing
    for _ in range(time_interval // log_interval):
        time.sleep(log_interval)
        print(f"Log at {time.time() - drone.start_time:.2f} seconds")

print(f"Drone {drone.id} has reached the target ({target_x:.6f}, {target_y:.6f})!")