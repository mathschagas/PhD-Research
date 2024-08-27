import random
import time
import math

class Mission:
    def __init__(self, mission_id, start_x, start_y, end_x, end_y):
        self.mission_id = mission_id
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.current_component = None

class Drone:
    def __init__(self, id, start_x, start_y):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.speed_kmh = 50.0
        self.distance_traveled = 0

    def move_towards(self, target_x, target_y):
        previous_x, previous_y = self.x, self.y
        distance_to_move = self.speed_kmh / 3600  # km per second
        distance_to_target = self.calculate_distance(self.x, self.y, target_x, target_y)
        ratio = distance_to_move / distance_to_target if distance_to_target != 0 else 0
        self.x += ratio * (target_x - self.x)
        self.y += ratio * (target_y - self.y)
        distance_moved = self.calculate_distance(previous_x, previous_y, self.x, self.y)
        self.distance_traveled += distance_moved
        return distance_moved

    def calculate_distance(self, x1, y1, x2, y2):
        R = 6371  # Earth radius in km
        lat1, lon1 = math.radians(x1), math.radians(y1)
        lat2, lon2 = math.radians(x2), math.radians(y2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def detect_uncertainty(self):
        # Simulate uncertainty occurrence
        return random.choice(["no_issue", "bad_weather", "restricted_airspace", "sensor_failure"])

class Car:
    def __init__(self, id, start_x, start_y):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.speed_kmh = 60.0  # Car speed is slightly higher

    def move_towards(self, target_x, target_y):
        previous_x, previous_y = self.x, self.y
        distance_to_move = self.speed_kmh / 3600  # km per second
        distance_to_target = self.calculate_distance(self.x, self.y, target_x, target_y)
        ratio = distance_to_move / distance_to_target if distance_to_target != 0 else 0
        self.x += ratio * (target_x - self.x)
        self.y += ratio * (target_y - self.y)
        distance_moved = self.calculate_distance(previous_x, previous_y, self.x, self.y)
        return distance_moved

    def calculate_distance(self, x1, y1, x2, y2):
        R = 6371  # Earth radius in km
        lat1, lon1 = math.radians(x1), math.radians(y1)
        lat2, lon2 = math.radians(x2), math.radians(y2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

class DelegationManager:
    def __init__(self):
        pass

    def choose_best_component(self, issue):
        # For now, let's always choose the Car if an issue occurs
        return Car(id=1, start_x=drone.x, start_y=drone.y)

# Define initial and final positions (30 km apart)
start_x, start_y = 51.5074, -0.1278  # London (example coordinates)
end_x, end_y = 51.5274, -0.1878  # Example 30 km away

# Create the mission and the drone
mission = Mission(mission_id=1, start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y)
drone = Drone(id=1, start_x=start_x, start_y=start_y)

# Assign the drone to the mission
mission.current_component = drone

# Simulation loop
while (round(drone.x, 4), round(drone.y, 4)) != (round(end_x, 4), round(end_y, 4)):
    moved_distance = drone.move_towards(end_x, end_y)
    print(f"Drone {drone.id} moved {moved_distance:.4f} km")

    # Detect uncertainty
    issue = drone.detect_uncertainty()
    if issue != "no_issue":
        print(f"Drone {drone.id} encountered an issue: {issue}. Delegating...")
        delegation_manager = DelegationManager()
        mission.current_component = delegation_manager.choose_best_component(issue)
        break

    # Simulate time passing
    time.sleep(1)

# If delegation happened, the car continues the mission
if isinstance(mission.current_component, Car):
    car = mission.current_component
    while (round(car.x, 4), round(car.y, 4)) != (round(end_x, 4), round(end_y, 4)):
        moved_distance = car.move_towards(end_x, end_y)
        print(f"Car {car.id} moved {moved_distance:.4f} km")

        # Simulate time passing
        time.sleep(1)

print(f"Mission {mission.mission_id} completed. Final position: ({end_x}, {end_y})")
