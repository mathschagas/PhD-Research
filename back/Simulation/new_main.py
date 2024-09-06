import requests

from UncertaintyMonitor import UncertaintyMonitor
from actor import Actor
from SimulationUtils import calculate_distance

# The list of uncertainties to simulate
uncertainties = [
    "internal_failure_drone",
    "internal_failure_car",
    "bad_weather",
    "restricted_area",
    "traffic_jam"
]

# Possible types of components
component_types = ["car", "drone", "bicycle", "truck", "pedestrian"]

# Start point (Wembley Stadium)
start_lat = 51.5560
start_lon = -0.2796

# after 5 km
percent25_lat = 51.5300
percent25_lon = -0.2090

# after 10 km
percent50_lat = 51.5160
percent50_lon = -0.1390

# after 15 km
percent75_lat = 51.5040
percent75_lon = -0.0730

# after 20 km (Tower Bridge)
end_lat = 51.5055
end_lon = -0.0754

lats = [start_lat, percent25_lat, percent50_lat, percent75_lat, end_lat]
lons = [start_lon, percent25_lon, percent50_lon, percent75_lon, end_lon]

# Define default speeds for each component type
component_speeds = {
    "car": 50.0,
    "drone": 60.0,
    "bicycle": 20.0,
    "truck": 40.0,
    "pedestrian": 5.0
}



def generate_components(components_config):

    # Clean the mock API
    response = requests.post("http://127.0.0.1:5001/clean_components")
    if response.status_code != 200:
        print(f"Failed to clean components. Status code: {response.status_code}, Message: {response.text}")

    # Generate components
    response = requests.post(
        "http://127.0.0.1:5001/generate_multiple_components",
        json=components_config
    )
    if response.status_code != 200:
        print(f"Failed to generate components. Status code: {response.status_code}, Message: {response.text}")
    else:
        print("Components generated successfully.")


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

def get_delegation_ranking(start_lat, start_lon, target_lat, target_lon):
    components = []
    response = requests.get(
        "http://127.0.0.1:5002/request_delegation/1/Default",
        params={"lat1": start_lat, "lon1": start_lon, "lat2": target_lat, "lon2": target_lon})
    if response.status_code == 200:
        components = response.json()
    else:
        print("Failed to get delegation ranking. Status code: {response.status_code}, Message: {response.text}")  
    return components

def uncertainty_affect_car(uncertainty):
    if uncertainty == "internal_failure_car" or uncertainty == "traffic_jam" or "restricted_area" in uncertainty:
        return True
    return False 


def get_support_network_config(num_types, quantity, uncertainty):
    if num_types == 1:  # Handle cases with only 1 type
        components_config = {
            'types': ["car"] if uncertainty_affect_car(uncertainty) else ["drone"],
            'quantity': quantity
        }
    else:
        components_config = {
            'types': component_types[num_types],
            'quantity': quantity
        }
    return components_config


if __name__ == "__main__":

    simulation_id = 1  # Start IDs from 1
    for uncertainty in uncertainties:
        for num_types in range(1, len(component_types) + 1):
            for quantity in [1, 5, 10]:      
                components_config = get_support_network_config(num_types, quantity, uncertainty)
                generate_components(components_config)
                for section in range(1, len(lats)-1):
                    reached_target = False
                    distance_to_target = 15.0 - 5.0 * (section - 1)
                    while not reached_target:
                        # Get the delegation ranking
                        delegation_ranking = get_delegation_ranking(lats[section], lons[section], end_lat, end_lon)
                        # Select the next component to delegate the task
                        if delegation_ranking:
                            next_component = delegation_ranking[0]
                            print(f"Delegating task to component {next_component['id']} ({next_component['type']})")
                        else:
                            print("No components available for delegation. Task failed.")
                            break


                        
