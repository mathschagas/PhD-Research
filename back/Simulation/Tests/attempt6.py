import random
import time
import math

class Actor:
    def __init__(self, id, start_x, start_y, speed_kmh):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.speed_kmh = speed_kmh  # Speed in km/h
        self.total_distance = 0
        self.distance_traveled = 0
        self.start_time = time.time()

    def move_towards(self, target_x, target_y, time_interval):
        previous_x, previous_y = self.x, self.y

        # Calculate the distance to move in this iteration based on speed and time interval
        distance_to_move = (self.speed_kmh / 3600) * time_interval  # Convert speed to km/s and multiply by time interval

        # Calculate the direction vector towards the target
        distance_to_target = self.calculate_distance(self.x, self.y, target_x, target_y)

        # Check if the actor is close enough to the destination to stop
        if distance_to_target <= distance_to_move:
            # Move directly to the destination and stop
            self.x = target_x
            self.y = target_y
            print(f"Actor {self.id} reached target location ({self.x:.6f}, {self.y:.6f})")
            return True  # Indicates that the actor has reached the destination

        # Otherwise, move normally towards the destination
        ratio = distance_to_move / distance_to_target if distance_to_target != 0 else 0
        self.x += ratio * (target_x - self.x)
        self.y += ratio * (target_y - self.y)

        # Calculate the distance moved in this iteration
        distance_moved = self.calculate_distance(previous_x, previous_y, self.x, self.y)
        self.distance_traveled += distance_moved

        elapsed_time = time.time() - self.start_time
        eta = self.estimated_time_to_arrival(target_x, target_y)

        print(f"Actor {self.id} moved to ({self.x:.6f}, {self.y:.6f})")
        print(f"Delivery time so far: {elapsed_time:.2f} seconds")
        print(f"Estimated time to delivery: {eta:.2f} seconds")
        print(f"Distance traveled so far: {self.distance_traveled:.6f} km")
        print(f"Distance to destination: {distance_to_target:.6f} km")
        print(f"Total route distance: {self.total_distance:.6f} km")
        print(f"Actor's speed: {self.speed_kmh:.2f} km/h")
        return False  # Indicates that the actor has not reached the destination

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
            return float('inf')  # In case the actor isn't moving

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
            print(f"Problem detected in: ({lat:.6f}, {lon:.6f})")
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

# Initial positions and target
start_x, start_y = random_position_within_london()
target_x, target_y = random_position_within_london()

# Create instances of Drone and Car using the Actor class
drone = Actor(id="Drone1", start_x=start_x, start_y=start_y, speed_kmh=60.0)
car = Actor(id="Car1", start_x=start_x, start_y=start_y, speed_kmh=50.0)

# Set the observer
observer = Observer()

# Calculate the total distance from start to target
drone.total_distance = drone.calculate_distance(start_x, start_y, target_x, target_y)
car.total_distance = drone.total_distance  # Assuming the car has the same target

print(f"Drone {drone.id} starting at ({drone.x:.6f}, {drone.y:.6f})")
print(f"Pickup Address: ({start_x:.6f}, {start_y:.6f})")
print(f"Target Address: ({target_x:.6f}, {target_y:.6f})")
print(f"Total distance to target: {drone.total_distance:.6f} km\n")

# Simulation loop with a configurable time interval
time_interval = 10  # seconds
log_interval = 1  # seconds

drone_reached_destination = False
while not drone_reached_destination:
    observer.detect_uncertainties()
    observer.report(drone.x, drone.y)

    if observer.conditions["bad_weather"]:
        print(f"Drone {drone.id} cannot proceed due to bad weather. Delegating to the car...")
        break
    elif observer.conditions["restricted_airspace"]:
        print(f"Drone {drone.id} cannot proceed due to restricted airspace. Delegating to the car...")
        break
    elif observer.conditions["sensor_failure"]:
        print(f"Drone {drone.id} experienced sensor failure. Delegating to the car...")
        break
    else:
        drone_reached_destination = drone.move_towards(target_x, target_y, time_interval)

    time.sleep(log_interval)

# If the drone cannot proceed, the car continues from the point where the drone stopped
car.x, car.y = drone.x, drone.y
car_reached_destination = False
while not car_reached_destination:
    car_reached_destination = car.move_towards(target_x, target_y, time_interval)
    time.sleep(log_interval)

print(f"Car {car.id} has reached the target ({target_x:.6f}, {target_y:.6f})!")