import requests
from datetime import datetime
import csv
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

# Create a session
session = requests.Session()

# Define a retry strategy
retry_strategy = Retry(
    total=20,  # Total number of retries
    backoff_factor=2,  # Waits 1 second between retries, then 2s, 4s, 8s...
    status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry on
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Methods to retry
)

# Mount the retry strategy to the session
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

scenarios = [
    "NoConstraintsBin",
    "NoConstraintsWeightedPrice",
    "NoConstraintsWeightedTimeToDeliver",
    "1ConstraintBin",
    "1ConstraintLikert",
    "2ConstraintsBin",
    "2ConstraintsLikert",
    "3ConstraintsBin",
    "3ConstraintsLikert",
    "HardConstraintsBin",
    "HardConstraintsLikert"
]

scenarios_random = [
    "NoConstraintsBin",
    "1ConstraintBin",
    "2ConstraintsBin",
    "3ConstraintsBin",
    "HardConstraintsBin",
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
# component_types = get_permutations()


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
    elif component_type == "truck":
        if uncertainty == "traffic_jam" or uncertainty == "restricted_area":
            return True
    elif component_type == "bicycle":
        if uncertainty == "bad_weather":
            return True
    elif component_type == "pedestrian":
        if uncertainty == "bad_weather":
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
    clean_response = session.post("http://127.0.0.1:5001/clean_components")
    if clean_response.status_code != 200:
        print(f"Failed to clean components. Status code: {clean_response.status_code}, Message: {clean_response.text}")

    # Generate components in the mock API
    for component_type in components_config['types']:
        gen_response = session.post(
            "http://127.0.0.1:5001/generate_components",
            json={"type": component_type, "quantity": components_config['count']}
        )
        if gen_response.status_code != 200:
            print(f"Failed to generate components of type {component_type}. Status code: {gen_response.status_code}, Message: {gen_response.text}")
            continue

    
    clean_tasks_response = session.put("http://127.0.0.1:5000/tasks/1", json={"registered_components": []})
    if clean_tasks_response.status_code != 200:
        print(f"Failed to clean tasks. Status code: {clean_tasks_response.status_code}, Message: {clean_tasks_response.text}")
    
    # Register tasks to all components in the mock network
    register_components_response = session.post(
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

    get_response = session.get("http://127.0.0.1:5000/tasks/1")
    return get_response.json()


# Get the best component from the Support Network
def get_delegation_component_from_sn(section, uncertainty, scenario = None, isRandom = False):

    # Initialize distance_to_target variable
    if section == "start":
        lat1, lon1 = start_x, start_y
    elif section == "middle":
        lat1, lon1 = middle_x, middle_y
    elif section == "end":
        lat1, lon1 = end_x, end_y
    lat2, lon2 = target_x, target_y
   
    # Get the best or random component from the Support Network
    url = f'http://127.0.0.1:5002/request_{"random_" if isRandom else ""}delegation/1/{scenario}' if scenario else f'http://127.0.0.1:5002/request_{"random_" if isRandom else ""}delegation/1/Fragile_Raining'
    response = session.get(url, params={"lat1": lat1, "lon1": lon1, "lat2": lat2, "lon2": lon2, "uncertainty": uncertainty})
    if response.status_code == 200:
        components = response.json()
        if components:
            selected_component = components[0]
            return selected_component, components
    return None, None


# Check if the delegated component was able to complete the task
def is_mission_completed(uncertainty, best_component, task, scenario):
    
    # If the component violates a hard constraint, the mission is considered incomplete
    for task_scenario in task['scenarios']:
        if task_scenario['name'] == scenario and 'constraints' in task_scenario:
            for constraint in task_scenario['constraints']:
                if constraint['weight'] > 5 and best_component is not None:
                    if best_component['raw_penalty'][constraint['name']] == 1:
                        return "No"

    mission_completed = "No"
    if not best_component:
        return mission_completed
    if "internal" in uncertainty:
        mission_completed = "Yes"
    elif not uncertainty_affects(component_type=best_component['type'], uncertainty=uncertainty):
        mission_completed = "Yes"
    return mission_completed


# Simulate the journey of a task
def simulate_journey(task, simulation_id, uncertainty, section, initial_actor, components_config, scenario, output_file_name="simulation_results.csv", isRandom = False):
    
    # Get component from the Support Network for delegation
    selected_component, components_list = get_delegation_component_from_sn(section, uncertainty=uncertainty, scenario=scenario, isRandom=isRandom)
    
    if not selected_component:
        print(f"No valid component found for delegation at simulation {simulation_id}.")

    # Record the simulation results
    with open(output_file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            simulation_id,
            uncertainty,
            section,
            initial_actor, 
            selected_component['id'] if selected_component else "-",
            selected_component['type'] if selected_component else "-", 
            selected_component['score'] if not isRandom and selected_component else "-",
            selected_component if selected_component else "-",
            ', '.join(components_config['types']),
            components_config['count'],
            json.dumps(components_list) if components_list else "-",
            json.dumps(task),
            is_mission_completed(best_component=selected_component, uncertainty=uncertainty, task=task, scenario=scenario)
        ])


def create_output_file(output_file_name="simulation_results.csv"):
    # Set up CSV to record results with reordered columns
    with open(output_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer = csv.writer(file)
        writer.writerow([
            'Simulation_ID',
            'Uncertainty_Type',
            'Trajectory_Section',
            'Initial_Actor',
            'Best_Component_ID',
            'Best_Component_Type',
            'Best_Component_Score',
            'Best_Component_Info',            
            'Component_Types',
            'Component_Quantities',
            'Ranking_Info',
            'Task_Info',
            'Mission_Completed'
        ])

# Run the simulations
def run_simulations(isRandom=False):
    current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # Set up CSV to record results with reordered columns
    results_dir_name = 'results/results_'+current_datetime
    os.makedirs(results_dir_name)

    sim_scenarios = scenarios_random if isRandom else scenarios

    for scenario in sim_scenarios:
        # Output file name
        output_file_name = f'{results_dir_name}/{scenario}.csv'
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
                        simulate_journey(task, simulation_id, uncertainty, section, initial_actor, components_config, scenario, output_file_name=output_file_name, isRandom=isRandom)
                        simulation_id += 1
        print(f"Simulations for \"{scenario}\" completed. Results are available in {output_file_name}.")

# Main function
if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Simulation started at: {start_time}")
    # run_simulations(isRandom=True)
    run_simulations()
    end_time = datetime.now()
    print(f"Simulation ended at: {end_time}")
    print(f"Total time taken: {end_time - start_time}")
