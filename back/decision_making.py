import requests as http_requests

def get_task(task_id):
    response = http_requests.get(f"http://127.0.0.1:5000/tasks/{task_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_component_info(component):
    response = http_requests.get(f"http://127.0.0.1:5001/components/{component['id']}/info")
    if response.status_code == 200:
        return response.json()['component']
    else:
        return None

# get component info for not mocked components
def _get_component_info(component):
    response = http_requests.get(f"http://127.0.0.1:{component['port']}/info")
    if response.status_code == 200:
        return response.json()['component']
    else:
        return None


def get_component_estimate(component, task):
    response = http_requests.get(f"http://127.0.0.1:{component['port']}/estimate")
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
    
    response = http_requests.get(url)
    
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

def calculate_weighted_scores(task, selectedScenario, quotes):
    # Initialize scores list
    scores = []
    components_to_remove = []

    matching_scenario = find_scenario_by_name(task['scenarios'], selectedScenario)
    if not matching_scenario:
        return scores
    
    # Iterate over each attribute in the task
    for attribute in matching_scenario['cbr_attributes']:
        # Get attribute details
        name = attribute['name']
        weight = attribute['weight']
        max_or_min = attribute['type']

        # Collect all estimates for this attribute
        all_estimates = [component['cbr'][name] for component in quotes]

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

    # Iterate over each constraint in the task
    for constraint in matching_scenario['constraints']:
        # Get constraint details
        name = constraint['name']
        operator = constraint['operator']
        value = constraint['value']
        weight = constraint['weight']

        for component in quotes:
            estimated_value = float(component['cbr'][name])
            value = float(value)

            raw_penalty = 0

            # Determine the penalty for each constraint
            if operator == 'less' and estimated_value >= value:
                raw_penalty =  1
            elif operator == 'greater' and estimated_value <= value:
                raw_penalty =  1
            elif operator == 'lessOrEqual' and estimated_value > value:
                raw_penalty =  1
            elif operator == 'greaterOrEqual' and estimated_value < value:
                raw_penalty =  1
            elif operator == 'equal' and value != estimated_value:
                raw_penalty =  1
            elif operator == 'notEqual' and value == estimated_value:
                raw_penalty =  1
            
            if 'raw_penalty' not in component:
                component['raw_penalty'] = {}
            component['raw_penalty'][name] = raw_penalty

            # Remove the component if the special constraint is not satisfied
            if weight == 999 and raw_penalty == 1:
                components_to_remove.append(component)
            else:
                # Apply the penalty by adding the weighted penalty from the score
                component['score'] += raw_penalty * weight

    # Remove the components that violated constraints with weight 999
    quotes = [comp for comp in quotes if comp not in components_to_remove]

    # Build final scores list
    for component in quotes:
        scores.append({
            "type": component['type'],
            "id": component['id'],
            "score": component['score'],
            "cbr": component['cbr'],
            "raw_penalty": component.get('raw_penalty', {})
        })

    return sorted(scores, key=lambda x: x['score'], reverse=False)

def calculate_delegation_cbr_score(task):

    # Check which components are registered for this task
    task_data = get_task(task['id'])
    registered_components = task_data.get('registered_components', [])

    for component in registered_components:
        component_info = get_component_info(component)
        if component_info:
            component.update(component_info)

    # Check which components are available
    available_components = [comp for comp in registered_components if comp.get('availability') == 'available']

    # Request estimates for the available components
    # estimates = [
    #     {
    #         "name": comp['name'],
    #         "port": comp['port'],
    #         "cbr": get_component_estimate(comp, task_data['id'])
    #     } 
    #     for comp in available_components
    # ]

    quotes = [
        {
            "type": comp['type'],
            "id": comp['id'],
            "cbr": get_component_quote(comp, task['start_location']['lat'], task['start_location']['lon'], task['end_location']['lat'], task['end_location']['lon'])
        } 
        for comp in available_components
    ]

    # Calculate score for each remaining component
    scores = calculate_weighted_scores(task_data, task['scenario'], quotes)
    # print(scores)
    return scores