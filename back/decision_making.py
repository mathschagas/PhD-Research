import requests as http_requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random

# Create a session
session = http_requests.Session()

# Define a retry strategy
retry_strategy = Retry(
    total=10,  # Total number of retries
    backoff_factor=1,  # Waits 1 second between retries, then 2s, 4s, 8s...
    status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry on
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Methods to retry
)

# Mount the retry strategy to the session
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)


def get_task(task_id):
    response = session.get(f"http://127.0.0.1:5000/tasks/{task_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_component_info(component):
    response = session.get(f"http://127.0.0.1:5001/components/{component['id']}/info")
    if response.status_code == 200:
        return response.json()['component']
    else:
        return None

# get component info for not mocked components
def _get_component_info(component):
    response = session.get(f"http://127.0.0.1:{component['port']}/info")
    if response.status_code == 200:
        return response.json()['component']
    else:
        return None


def get_component_estimate(component, task):
    response = session.get(f"http://127.0.0.1:{component['port']}/estimate")
    if response.status_code == 200:
        return response.json()['cbr']
    else:
        return None

def get_component_quote(component, lat1, lon1, lat2, lon2):
    url = (
        f"http://127.0.0.1:5001/components/{component['id']}/quote"
        f"?lat1={lat1}&lon1={lon1}"
        f"&lat2={lat2}&lon2={lon2}"
    )
    
    response = session.get(url)
    if response.status_code == 200:
        return response.json().get('cbr')
    else:
        return None


def find_scenario_by_name(scenarios, selectedScenario):
    for scenario in scenarios:
        if scenario['name'] == selectedScenario:
            return scenario
    return None

def normalize(value, min_value, max_value, minimize=False):
    if max_value == min_value:
        return 0
    else:
        normalized = (value - min_value) / (max_value - min_value)
        return normalized if minimize else 1 - normalized

# Returns True if the uncertainty affects the component type
def uncertainty_affects(uncertainty, component_type):
    if component_type == "car" or component_type == "truck":
        if uncertainty == "traffic_jam" or uncertainty == "restricted_area":
            return True
    elif component_type == "drone" or component_type == "pedestrian" or component_type == "bicycle":
        if uncertainty == "bad_weather":
            return True
    return False

def calculate_weighted_scores(task, selectedScenario, quotes, uncertainty):
    # Initialize scores list
    scores = []
    components_to_remove = []

    matching_scenario = find_scenario_by_name(task['scenarios'], selectedScenario)
    if not matching_scenario:
        return scores
    
    # Remove components that their type is affected by the current uncertainty
    for comp in quotes:
        if uncertainty_affects(uncertainty, comp['type']):
            components_to_remove.append(comp)

    # Remove the components that violated constraints with weight 999
    quotes = [comp for comp in quotes if comp not in components_to_remove]
    components_to_remove = []

    # Iterate over each constraint in the task
    if 'constraints' in matching_scenario:
        for constraint in matching_scenario['constraints']:
            # Get constraint details
            name = constraint['name']
            operator = constraint['operator']
            value = constraint['value']
            weight = constraint['weight']

            for component in quotes:
                estimated_value = float(component['cbr'][name])
                value = float(value)

                # Define a dictionary to map operators to lambda functions
                operator_functions = {
                    'less': lambda est, val: est >= val,
                    'greater': lambda est, val: est <= val,
                    'lessOrEqual': lambda est, val: est > val,
                    'greaterOrEqual': lambda est, val: est < val,
                    'equal': lambda est, val: est != val,
                    'notEqual': lambda est, val: est == val
                }

                # Determine the penalty for each constraint
                raw_penalty = 1 if operator_functions[operator](estimated_value, value) else 0
                
                if 'raw_penalty' not in component:
                    component['raw_penalty'] = {}
                component['raw_penalty'][name] = raw_penalty

                # Remove the component if the special constraint is not satisfied
                if weight > 5 and raw_penalty == 1:
                    components_to_remove.append(component)
                else:
                    # Apply the penalty by adding the weighted penalty from the score
                    component['score'] = component.get('score', 0) + raw_penalty * weight


    # Remove the components that violated constraints with weight 999
    quotes = [comp for comp in quotes if comp not in components_to_remove]

    if len(quotes) == 0:
        return scores
    
    # Iterate over each attribute in the task
    for attribute in matching_scenario['cbr_attributes']:
        # Get attribute details
        name = attribute['name']
        weight = attribute['weight']
        max_or_min = attribute['type']

        # Collect all estimates for this attribute
        all_estimates = [component['cbr'][name] for component in quotes]

        if not all_estimates:
            # Calculate min and max values
            min_value = min(all_estimates)
            max_value = max(all_estimates)

            # Iterate over each component in estimates
            for component in quotes:
                # Get the estimate value for this attribute from the component
                estimated_value = component['cbr'][name]

                # Normalize the estimate value
                normalized_value = normalize(estimated_value, min_value, max_value, max_or_min == 'min')

                # Add the weighted attribute to the score
                component['score'] = component.get('score', 0) + weight * normalized_value

    # Build final scores list
    for component in quotes:
        scores.append({
            "type": component['type'],
            "id": component['id'],
            "score": component['score'] if 'score' in component else 0,
            "cbr": component['cbr'],
            "raw_penalty": component.get('raw_penalty', {})
        })

    return sorted(scores, key=lambda x: x['score'], reverse=False)

def calculate_delegation_cbr_score(task, uncertainty, isRandom=False):

    # Check which components are registered for this task
    task_data = get_task(task['id'])
    registered_components = task_data.get('registered_components', [])

    for component in registered_components:
        component_info = get_component_info(component)
        if component_info:
            component.update(component_info)

    # Check which components are available
    available_components = [comp for comp in registered_components if comp.get('availability') == 'available']

    quotes = [
        {
            "type": comp['type'],
            "id": comp['id'],
            "cbr": get_component_quote(comp, task['start_location']['lat'], task['start_location']['lon'], task['end_location']['lat'], task['end_location']['lon'])
        } 
        for comp in available_components
    ]

    # Calculate score for each remaining component
    if isRandom:
        random.shuffle(quotes)
        scores = quotes
    else:
        scores = calculate_weighted_scores(task_data, task['scenario'], quotes, uncertainty)

    return scores