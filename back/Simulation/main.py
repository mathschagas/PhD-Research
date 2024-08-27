import time

from SimulationUtils import random_position_within_london_30km, calculate_distance
from UncertaintyMonitor import UncertaintyMonitor
from Actor import Actor

# Initial positions and target
start_x, start_y = random_position_within_london_30km()
target_x, target_y = random_position_within_london_30km()

# Create instances of Drone and Car using the Actor class
drone = Actor(id="Drone1", start_x=start_x, start_y=start_y, speed_kmh=60.0)

# Set the observer
observer = UncertaintyMonitor()
observer.set_actor(drone.id)

# Calculate the total distance from start to target
drone.total_distance = calculate_distance(start_x, start_y, target_x, target_y)

print(f"Actor with ID {drone.id} starting at ({drone.x:.6f}, {drone.y:.6f})")
print(f"Pickup Address: ({start_x:.6f}, {start_y:.6f})")
print(f"Target Address: ({target_x:.6f}, {target_y:.6f})")
print(f"Total distance to target: {drone.total_distance:.6f} km\n")

# Simulation loop with a configurable time interval
time_interval = 60  # seconds
log_interval = 1  # seconds

reached_destination = False
while not reached_destination:
    observer.detect_uncertainties()
    observer.report(drone.x, drone.y)

    if observer.conditions["bad_weather"]:
        print(f"Actor with ID {drone.id} cannot proceed due to bad weather. Requesting Delegation...")
        break
    elif observer.conditions["restricted_airspace"]:
        print(f"Actor with ID {drone.id} cannot proceed due to bad weather. Requesting Delegation...")
        break
    elif observer.conditions["sensor_failure"]:
        print(f"Actor with ID {drone.id} cannot proceed due to bad weather. Requesting Delegation...")
        break
    else:
        reached_destination = drone.move_towards(target_x, target_y, time_interval)

    time.sleep(log_interval)

if not reached_destination:

    # If the drone cannot proceed, the car continues from the point where the drone stopped
    car = Actor(id="Car1", start_x=start_x, start_y=start_y, speed_kmh=50.0)
    observer.set_actor(car.id)
    car.total_distance = drone.total_distance  # Assuming the car has the same target

    car.x, car.y = drone.x, drone.y
    while not reached_destination:
        reached_destination = car.move_towards(target_x, target_y, time_interval)
        time.sleep(log_interval)