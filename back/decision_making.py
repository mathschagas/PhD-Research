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
    
def calculate_weighted_scores(task, estimates):
    # Initialize scores list
    scores = []

    # Iterate over each attribute in the task
    for attribute in task['cbr_attributes']:
        # Get attribute details
        name = attribute['name']
        weight = attribute['weight']
        max_or_min = attribute['max_or_min']

        # If the attribute is 'rating', skip it
        if name == 'rating':
            continue

        # Collect all estimates for this attribute
        all_estimates = [component['cbr'][name] for component in estimates]

        # Calculate min and max values
        min_value = min(all_estimates)
        max_value = max(all_estimates)

        # Iterate over each component in estimates
        for component in estimates:
            # Get the estimate value for this attribute from the component
            estimate_value = component['cbr'][name]

            # Normalize the estimate value
            if max_or_min == 'min':
                # For minimization, subtract the min value and divide by the range
                normalized_value = (estimate_value - min_value) / (max_value - min_value) if max_value != min_value else 0
            else:
                # For maximization, subtract the min value and divide by the range
                normalized_value = (estimate_value - min_value) / (max_value - min_value) if max_value != min_value else 1

            # Add the weighted attribute to the score
            component['score'] = component.get('score', 0) + weight * normalized_value

    # Build scores list
    for component in estimates:
        scores.append({"name": component['name'], "score": component['score']})

    return sorted(scores, key=lambda x: x['score'], reverse=True)

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

    # Filter out components that present estimates that violate the constraints
    # valid_components = [comp for comp, est in zip(available_components, estimates) if est <= constraints]

    # Calculate score for each remaining component
    scores = calculate_weighted_scores(task_data, estimates)
    # print(scores)
    return scores