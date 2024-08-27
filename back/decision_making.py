import requests as http_requests

def get_task(task_id):
    response = http_requests.get(f"http://127.0.0.1:5000/tasks/{task_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_component_info(component):
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
    
def find_scenario_by_name(scenarios, selectedScenario):
    for scenario in scenarios:
        if scenario['name'] == selectedScenario:
            return scenario
    return None

def normalize(value, min_value, max_value, minimize=False):
    normalized = (value - min_value) / (max_value - min_value)
    return normalized if minimize else 1 - normalized

def calculate_weighted_scores(task, selectedScenario, estimates):
    # Initialize scores list
    scores = []

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
        all_estimates = [component['cbr'][name] for component in estimates]

        # Calculate min and max values
        min_value = min(all_estimates)
        max_value = max(all_estimates)

        # Iterate over each component in estimates
        for component in estimates:
            # Get the estimate value for this attribute from the component
            estimated_value = component['cbr'][name]

            # Normalize the estimate value
            normalized_value = normalize(estimated_value, min_value, max_value, max_or_min == 'min')

            # Add the weighted attribute to the score
            component['score'] = component.get('score', 0) + weight * normalized_value

            for constraint in matching_scenario['constraints']:
                # Get constraint details
                name = constraint['name']
                print(name)
                operator = constraint['operator']
                value = constraint['value']
                weight = constraint['weight']

                estimated_value = float(estimated_value)
                value = float(value)

                raw_penalty = 0
                # Determine the penalty for each constraint
                if operator == 'less' and estimated_value >= value:
                    raw_penalty =  abs(estimated_value - value)
                elif operator == 'greater' and estimated_value <= value:
                    raw_penalty =  abs(estimated_value - value)
                elif operator == 'lessOrEqual' and estimated_value > value:
                    raw_penalty =  abs(estimated_value - value)
                elif operator == 'greaterOrEqual' and estimated_value < value:
                    raw_penalty =  abs(estimated_value - value)
                elif operator == 'equal' and value != estimated_value:
                    raw_penalty =  1
                elif operator == 'notEqual' and value == estimated_value:
                    raw_penalty =  1
                
                if 'raw_penalty' not in component:
                   component['raw_penalty'] = {}
                component['raw_penalty'][name] = raw_penalty

    # Build scores list
    for component in estimates:
        scores.append({"name": component['name'], "score": component['score'] + component.get('raw_penalty', {}).get('price', 0)})

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
    estimates = [
        {
            "name": comp['name'],
            "port": comp['port'],
            "cbr": get_component_estimate(comp, task_data['id'])
        } 
        for comp in available_components
    ]

    # Calculate score for each remaining component
    scores = calculate_weighted_scores(task_data, task['scenario'], estimates)
    # print(scores)
    return scores