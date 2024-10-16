import time
import requests
from SimulationUtils import calculate_distance
from UncertaintyMonitor import UncertaintyMonitor
from actor import Actor
import csv
import json
from datetime import datetime
import random

# Output file name for simulation results
output_file_name = f'simulation_results_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.csv'

# The list of uncertainties to simulate
uncertainties = [
    # "internal_failure_drone",
    # "internal_failure_car",
    "bad_weather",
    # "restricted_area",
    # "traffic_jam"
]

# Possible types of components
component_types = {
    1: ["drone"],  # For uncertainties affecting drones only
    2: ["drone", "car"],
    3: ["drone", "car", "bicycle"],
    4: ["drone", "car", "bicycle", "truck"],
    5: ["drone", "car", "bicycle", "truck", "pedestrian"]
}

# Define default speeds for each component type
component_speeds = {
    "car": 50.0,
    "drone": 60.0,
    "bicycle": 20.0,
    "truck": 40.0,
    "pedestrian": 5.0
}

# Set up CSV to record results with reordered columns
with open(output_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Simulation_ID', 'Uncertainty_Type', 'Trajectory_Section', 'Actor_ID',
        'Location_Info', 'CBR_Value', 'Component_Types', 'Component_Quantities',
        'Delegation_Order', 'Ranking_Info', 'Task_Info', 'Mission_Completed'
    ])

def get_best_component_from_support_network(start_x, start_y, target_x, target_y):
    response = requests.get(
        "http://127.0.0.1:5002/request_delegation/1/Fragile_Raining",
        params={"lat1": start_x, "lon1": start_y, "lat2": target_x, "lon2": target_y}
    )
    if response.status_code == 200:
        components = response.json()
        if components:
            best_component_info = components[0]
            return best_component_info['id'], best_component_info['score'], best_component_info['type'], components
    return None, None, None, None

def get_random_component_from_support_network(start_x, start_y, target_x, target_y):
    response = requests.get(
        "http://127.0.0.1:5002/request_delegation/1/Fragile_Raining",
        params={"lat1": start_x, "lon1": start_y, "lat2": target_x, "lon2": target_y}
    )
    if response.status_code == 200:
        components = response.json()
        if components:
            random_component_info = random.choice(components)
            return random_component_info['id'], random_component_info['score'], random_component_info['type'], components
    return None, None, None, None

# Function to simulate the journey and trigger delegation at a specific section
def simulate_journey(task, simulation_id, uncertainty, section, actor: Actor, uncertainty_monitor: UncertaintyMonitor, start_x, start_y, target_x, target_y, components_config, time_interval=60, speed_multiplier=1):
    reached_destination = False
    best_cbr = None
    delegation_order = 1  # Start with the first delegation
    initial_lat = start_x
    initial_lon = start_y
    final_lat = None
    final_lon = None
    mission_completed = False
    trajectory_section = section  # Store the section of the trajectory

    first_section_end = actor.total_distance / 4
    second_section_end = actor.total_distance / 2
    third_section_end = 3 * actor.total_distance / 4

    # Initialize distance_to_target variable
    distance_to_target = calculate_distance(actor.x, actor.y, target_x, target_y)

    while not reached_destination:
        current_distance_traveled = actor.distance_traveled

        # Force the occurrence of uncertainty at a random point within the specified section
        if section == "start" and current_distance_traveled >= first_section_end:
            uncertainty_monitor.force_uncertainty(uncertainty)
        elif section == "middle" and current_distance_traveled >= second_section_end:
            uncertainty_monitor.force_uncertainty(uncertainty)
        elif section == "end" and current_distance_traveled >= third_section_end:
            uncertainty_monitor.force_uncertainty(uncertainty)

        uncertainty_monitor.report(actor.x, actor.y)

        # Recalculate distance to target only if an uncertainty occurs
        if any(uncertainty_monitor.conditions.values()):
            distance_to_target = calculate_distance(actor.x, actor.y, target_x, target_y)
            final_lat = actor.x
            final_lon = actor.y

            # Get the best component from the support network manager
            best_component_name, best_cbr, best_component_type, ranking = get_best_component_from_support_network(actor.x, actor.y, target_x, target_y)

            if best_component_name is not None:
                speed_kmh = component_speeds.get(best_component_type, 50.0)
                
                location_info = {
                    "start": {"lat": initial_lat, "lon": initial_lon},
                    "end": {"lat": final_lat, "lon": final_lon},
                    "distance_traveled_km": round(actor.distance_traveled, 6),
                    "distance_to_target_km": round(distance_to_target, 6)
                }

                with open(output_file_name, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        simulation_id, uncertainty, trajectory_section, actor.id,
                        json.dumps(location_info), best_cbr, ', '.join(components_config['types']), components_config['count'],
                        delegation_order, json.dumps(ranking), json.dumps(task), "No"
                    ])

                best_component = Actor(id=best_component_name, start_x=actor.x, start_y=actor.y, speed_kmh=speed_kmh)
                uncertainty_monitor.set_actor(best_component.id)
                delegation_order += 1
                reached_destination = best_component.move_towards(target_x, target_y, time_interval)
                initial_lat = final_lat
                initial_lon = final_lon
                final_lat = target_x
                final_lon = target_y
                mission_completed = True
                break
            else:
                # Handle the case where no valid component is found (e.g., due to violations of hard constraints)
                print(f"No valid component found for delegation at ({actor.x:.6f}, {actor.y:.6f})")

                # Record with empty values and "-" for the CBR-dependent fields
                with open(output_file_name, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        simulation_id, uncertainty, trajectory_section, actor.id,
                        "-", "-", ', '.join(components_config['types']), components_config['count'],
                        delegation_order, "-", json.dumps(task), "No"
                    ])
                break

        else:
            reached_destination = actor.move_towards(target_x, target_y, time_interval)
        
        time.sleep(1 / speed_multiplier)

    # Ensure location_info is defined for the final record
    if 'location_info' not in locals():
        location_info = {
            "start": {"lat": initial_lat, "lon": initial_lon},
            "end": {"lat": target_x, "lon": target_y},
            "distance_traveled_km": round(actor.distance_traveled, 6),
            "distance_to_target_km": 0.0  # Mission completed, so distance to target is 0
        }

    # Update distance_to_target_km to 0 when the mission is completed
    location_info["distance_to_target_km"] = 0.0 if mission_completed else distance_to_target

    # Record the final actor's segment
    with open(output_file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            simulation_id, uncertainty, trajectory_section, 
            best_component.id if 'best_component' in locals() and best_component is not None else actor.id,
            json.dumps(location_info), best_cbr if best_cbr is not None else "-", 
            ', '.join(components_config['types']), components_config['count'],
            delegation_order, json.dumps(ranking if 'ranking' in locals() else "-"), json.dumps(task), "Yes" if mission_completed else "No"
        ])

def uncertainty_affect_car(uncertainty):
    if uncertainty == "internal_failure_car" or uncertainty == "traffic_jam" or "restricted_area" in uncertainty:
        return True
    return False 

def register_tasks_to_all():
    
    response = requests.put("http://127.0.0.1:5000/tasks/1", json={"registered_components": []})
    if response.status_code != 200:
        print(f"Failed to clean tasks. Status code: {response.status_code}, Message: {response.text}")
    
    # Register tasks to all components in the mock network
    response = requests.post(
        "http://127.0.0.1:5001/register_tasks_to_all",
        json={
            "tasks": [
                {"id": "1", "name": "Deliver package"}
            ]
        }
    )
    if response.status_code == 200:
        print("Tasks registered to all components successfully.")
    else:
        print(f"Failed to register tasks. Status code: {response.status_code}, Message: {response.text}")

    response = requests.get("http://127.0.0.1:5000/tasks/1")
    return response.json()

# Run the simulations
simulation_id = 1  # Start IDs from 1
for uncertainty in uncertainties:
    for num_types in range(1, len(component_types)+1):  # Number of types from 1 to 5
        for count in [20]:  # Number of components of each type
            if num_types == 1:  # Handle cases with only 1 type
                if uncertainty_affect_car(uncertainty):
                    components_config = {
                        'types': ["car"],
                        'count': count
                    }
                else:
                    components_config = {
                        'types': ["drone"],
                        'count': count
                    }
            else:
                components_config = {
                    'types': component_types[num_types],
                    'count': count
                }

            # Clean the mock API
            response = requests.post("http://127.0.0.1:5001/clean_components")
            if response.status_code != 200:
                print(f"Failed to clean components. Status code: {response.status_code}, Message: {response.text}")
                continue

            # Generate components in the mock API
            for component_type in components_config['types']:
                response = requests.post(
                    "http://127.0.0.1:5001/generate_components",
                    json={"type": component_type, "quantity": components_config['count']}
                )
                if response.status_code != 200:
                    print(f"Failed to generate components of type {component_type}. Status code: {response.status_code}, Message: {response.text}")
                    continue

            # Register tasks to all components
            task = register_tasks_to_all()

            # Initial positions and target with a distance of approximately 20 km
            start_x, start_y = 51.5103, -0.1277  # Trafalgar Square area
            target_x, target_y = 51.3890, -0.2010  # Sutton area

            # Select initial actor based on uncertainty
            if uncertainty_affect_car(uncertainty):
                actor = Actor(id="InitialCar", start_x=start_x, start_y=start_y, speed_kmh=component_speeds["car"])
            else:
                actor = Actor(id="InitialDrone", start_x=start_x, start_y=start_y, speed_kmh=component_speeds["drone"])

            # Set the observer
            uncertainty_monitor = UncertaintyMonitor()
            uncertainty_monitor.set_actor(actor.id)

            # Calculate the total distance from start to target
            actor.total_distance = calculate_distance(start_x, start_y, target_x, target_y)

            print(f"Actor with ID {actor.id} starting at ({actor.x:.6f}, {actor.y:.6f})")
            print(f"Pickup Address: ({start_x:.6f}, {start_y:.6f})")
            print(f"Target Address: ({target_x:.6f}, {target_y:.6f})")
            print(f"Total distance to target: {actor.total_distance:.6f} km\n")

            # Simulate for each section of the journey
            for section in ["start", "middle", "end"]:
                simulate_journey(task, simulation_id, uncertainty, section, actor, uncertainty_monitor, start_x, start_y, target_x, target_y, components_config, speed_multiplier=1000)
                simulation_id += 1

print(f"Simulation completed. Results are saved in {output_file_name}.")
