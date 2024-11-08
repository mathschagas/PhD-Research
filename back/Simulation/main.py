import requests
from datetime import datetime
import csv
import json

scenarios = [
    # "NoConstraintsBin"
    # "NoConstraintsWeightedPrice"
    # "NoConstraintsWeightedTimeToDeliver"
    # "1ConstraintBin"
    # "1ConstraintLikert"
    # "2ConstraintsBin"
    # "2ConstraintsLikert"
    "3ConstraintsBin"
    # "3ConstraintsLikert"
    # "HardConstraintsBin"
    # "HardConstraintsLikert"
]

# The list of uncertainties to simulate
uncertainties = [
    "internal_failure_drone",
    "internal_failure_car",
    "bad_weather",
    "restricted_area",
    "traffic_jam",
]

# Possible types of components
component_types = {
    1: ["drone"],  # For uncertainties affecting drones only
    2: ["drone", "car"],
    3: ["drone", "car", "bicycle"],
    4: ["drone", "car", "bicycle", "truck"],
    5: ["drone", "car", "bicycle", "truck", "pedestrian"]
}

# Possible number of components for each type
num_components = [1, 5, 10]

# Latitudes and longitudes for the origin, target, start, middle and end points
origin_x, origin_y = 51.5103, -0.1277  
target_x, target_y = 51.3450, -0.2415  
start_x, start_y = 51.4690, -0.1562
middle_x, middle_y = 51.4277, -0.1847
end_x, end_y = 51.3864, -0.2131

# Returns True if the uncertainty affects the component type
def uncertainty_affects(uncertainty, component_type):
    if component_type == "car":
        if uncertainty == "traffic_jam" or uncertainty == "restricted_area" or uncertainty == "internal_failure_car":
            return True
    elif component_type == "drone":
        if uncertainty == "bad_weather" or uncertainty == "internal_failure_drone":
            return True
    return False


# Returns the types included in a simulation based on the number of types and the uncertainty
def get_types_for_simulation(num_types, uncertainty):
    if num_types == 1:
        if uncertainty_affects(uncertainty, "drone"):
            return ["drone"]
        elif uncertainty_affects(uncertainty, "car"):
            return ["car"]
    return component_types[num_types]


# Set the environment APIs for the simulation
def set_environment_apis(components_config):

    # Clean the components in the mock API
    clean_response = requests.post("http://127.0.0.1:5001/clean_components")
    if clean_response.status_code != 200:
        print(f"Failed to clean components. Status code: {clean_response.status_code}, Message: {clean_response.text}")

    # Generate components in the mock API
    for component_type in components_config['types']:
        gen_response = requests.post(
            "http://127.0.0.1:5001/generate_components",
            json={"type": component_type, "quantity": components_config['count']}
        )
        if gen_response.status_code != 200:
            print(f"Failed to generate components of type {component_type}. Status code: {gen_response.status_code}, Message: {gen_response.text}")
            continue

    
    clean_tasks_response = requests.put("http://127.0.0.1:5000/tasks/1", json={"registered_components": []})
    if clean_tasks_response.status_code != 200:
        print(f"Failed to clean tasks. Status code: {clean_tasks_response.status_code}, Message: {clean_tasks_response.text}")
    
    # Register tasks to all components in the mock network
    register_components_response = requests.post(
        "http://127.0.0.1:5001/register_tasks_to_all",
        json={
            "tasks": [
                {"id": "1", "name": "Deliver package"}
            ]
        }
    )
    if register_components_response.status_code == 200:
        pass
        # print("Tasks registered to all components successfully.")
    else:
        print(f"Failed to register tasks. Status code: {register_components_response.status_code}, Message: {register_components_response.text}")

    get_response = requests.get("http://127.0.0.1:5000/tasks/1")
    return get_response.json()


# Get the best component from the Support Network
def get_best_component_from_sn(section, scenario = None):

    # Initialize distance_to_target variable
    if section == "start":
        lat1, lon1 = start_x, start_y
    elif section == "middle":
        lat1, lon1 = middle_x, middle_y
    elif section == "end":
        lat1, lon1 = end_x, end_y
    lat2, lon2 = target_x, target_y
   
    # Get the best component from the Support Network
    url = f"http://127.0.0.1:5002/request_delegation/1/{scenario}" if scenario else "http://127.0.0.1:5002/request_delegation/1/Fragile_Raining"
    response = requests.get(url, params={"lat1": lat1, "lon1": lon1, "lat2": lat2, "lon2": lon2})
    if response.status_code == 200:
        components = response.json()
        if components:
            best_component = components[0]
            return best_component, components
    return None, None


# Check if the delegated component was able to complete the task
def is_mission_completed(uncertainty, best_component):
    mission_completed = "No"
    if not best_component:
        return mission_completed
    if "internal" in uncertainty:
        mission_completed = "Yes"
    elif not uncertainty_affects(component_type=best_component['type'], uncertainty=uncertainty):
        mission_completed = "Yes"
    return mission_completed


# Simulate the journey of a task
def simulate_journey(task, simulation_id, uncertainty, section, initial_actor, components_config, scenario, output_file_name="simulation_results.csv"):
    # Get the best component from the Support Network
    best_component, ranking = get_best_component_from_sn(section, scenario=scenario)
    if not best_component:
        print(f"No valid component found for delegation at section = {section} in the journey.")

    # Record the simulation results
    with open(output_file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            simulation_id,
            uncertainty,
            section,
            initial_actor, 
            best_component['id'] if best_component else initial_actor,
            best_component['type'] if best_component else "-", 
            best_component['score'] if best_component else "-",
            ', '.join(components_config['types']),
            components_config['count'],
            json.dumps(ranking) if ranking else "-",
            json.dumps(task),
            is_mission_completed(best_component=best_component, uncertainty=uncertainty)
        ])


def create_output_file(output_file_name="simulation_results.csv"):
    # Set up CSV to record results with reordered columns
    with open(output_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Simulation_ID',
            'Uncertainty_Type',
            'Trajectory_Section',
            'Initial_Actor',
            'Best_Component_ID',
            'Best_Component_Type',
            'CBR_Value',
            'Component_Types',
            'Component_Quantities',
            'Ranking_Info',
            'Task_Info',
            'Mission_Completed'
        ])

# Run the simulations
def run_simulations():
    current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    for scenario in scenarios:
        # Output file name
        output_file_name = f'{scenario}_{current_datetime}.csv'
        create_output_file(output_file_name=output_file_name)
        simulation_id = 1 # Start IDs from 1
        # For each type of uncertainty
        for uncertainty in uncertainties:
            # For each number of component types (1, 2, 3, 4, 5)
            for num_types in range(1, len(component_types)+1):
                # For each different amount of components within each type
                for count in num_components:
                    components_config = {
                        'types': get_types_for_simulation(num_types, uncertainty),
                        'count': count
                    }
                    task = set_environment_apis(components_config)
                    initial_actor = "InitialDrone" if uncertainty_affects(uncertainty, "drone") else "InitialCar"
                    # For each section of the journey
                    for section in ["start", "middle", "end"]:
                        simulate_journey(task, simulation_id, uncertainty, section, initial_actor, components_config, scenario, output_file_name=output_file_name)
                        simulation_id += 1
        print(f"Simulations for \"{scenario}\" completed. Results are available in {output_file_name}.")

# Main function
if __name__ == "__main__":
    run_simulations()

