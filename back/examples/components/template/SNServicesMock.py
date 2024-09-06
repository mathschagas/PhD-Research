from datetime import datetime
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import requests as http_requests

from quote_functions import quote_functions

app = Flask(__name__)
CORS(app)

# In-memory store for simulated components
components = {}

# URL of the task management API
TASK_MANAGEMENT_API_URL = 'http://127.0.0.1:5000/tasks/bulk_update'

@app.route('/generate_components', methods=['POST'])
def generate_components():
    data = request.get_json()
    component_type = data.get('type')
    quantity = data.get('quantity', 1)

    generated_components = []

    for i in range(quantity):
        component_id = str("sn_")+str(component_type)+str(i+1)  # Unique ID for each component
        new_component = {
            'id': component_id,
            'type': component_type,
            'availability': "available",
            'registered_tasks': []
        }
        components[component_id] = new_component
        generated_components.append(new_component)

    return jsonify(status='OK', message=f'{quantity} components of type {component_type} generated successfully.', components=generated_components)


@app.route('/generate_multiple_components', methods=['POST'])
def generate_multiple_components():
    data = request.get_json()
    components_to_generate = data.get('components', [])

    generated_components = []

    for component_request in components_to_generate:
        component_type = component_request.get('type')
        quantity = component_request.get('quantity', 1)

        if not component_type:
            return jsonify(status='Error', message='Component type is missing for one or more entries'), 400

        for _ in range(quantity):
            component_id = str(uuid.uuid4())
            new_component = {
                'id': component_id,
                'type': component_type,
                'availability': "available",
                'registered_tasks': []
            }
            components[component_id] = new_component
            generated_components.append(new_component)

    return jsonify(status='OK', message=f'Components generated successfully.', components=generated_components)


@app.route('/components/all', methods=['GET'])
def get_all_components():
    if not components:
        return jsonify(status='Error', message='No components found'), 404

    return jsonify(status='OK', components=list(components.values()))


@app.route('/clean_components', methods=['POST'])
def clear_all_components():
    global components
    components.clear()
    return jsonify(status='OK', message='All components have been cleared.')


@app.route('/components/<component_id>/status', methods=['GET'])
def get_component_status(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    return jsonify(status='OK', availability=component['availability'])


@app.route('/components/<component_id>/info', methods=['GET'])
def get_component_info(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    return jsonify(status='OK', component=component)


@app.route('/components/<component_id>/update_info', methods=['PUT'])
def update_component_info(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    data = request.get_json()
    if 'availability' in data:
        component['availability'] = data['availability']
    if 'registered_tasks' in data:
        component['registered_tasks'] = data['registered_tasks']

    return jsonify(status='OK', message='Component information updated successfully')


@app.route('/components/<component_id>/register_tasks', methods=['POST'])
def register_tasks(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    tasks = request.get_json()
    component['registered_tasks'] = tasks
    registered_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Update the task management API
    component_info = {'id': component_id, 'type': component['type']}
    tasks_data = [{'id': task['id'], 'registered_components': [component_info]} for task in tasks]
    response = http_requests.put(TASK_MANAGEMENT_API_URL, json=tasks_data)

    if response.status_code != 200:
        return jsonify(status='ERROR', message='Failed to update tasks in the task management API')

    return jsonify(status='OK', registered_time=registered_time, message='Tasks registered successfully')


@app.route('/register_tasks_to_all', methods=['POST'])
def register_tasks_to_all():
    tasks = request.get_json().get('tasks', [])
    if not tasks:
        return jsonify(status='Error', message='No tasks provided'), 400

    for component_id, component in components.items():
        component['registered_tasks'].extend(tasks)

    # Update the task management API for all components
    for component_id, component in components.items():
        component_info = {'id': component_id, 'type': component['type']}
        tasks_data = [{'id': task['id'], 'registered_components': [component_info]} for task in tasks]
        response = http_requests.put(TASK_MANAGEMENT_API_URL, json=tasks_data)

        if response.status_code != 200:
            return jsonify(status='ERROR', message=f'Failed to update tasks for component {component_id} in the task management API')

    return jsonify(status='OK', message='Tasks assigned to all components successfully')


@app.route('/components/<component_id>/remove_task', methods=['DELETE'])
def remove_task(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    task_id = request.get_json().get('id')
    task_to_remove = None
    for task in component['registered_tasks']:
        if task.get('id') == task_id:
            task_to_remove = task
            break

    if task_to_remove:
        component['registered_tasks'].remove(task_to_remove)
        return jsonify(status='OK', message=f'Task with id {task_id} removed successfully.')
    else:
        return jsonify(status='Error', message=f'Task with id {task_id} not found.')


@app.route('/components/<component_id>/randomize', methods=['GET'])
def randomize_availability(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    component['availability'] = random.choice(["available", "unavailable"])
    return jsonify(status=component['availability'])


@app.route('/components/<component_id>/quote', methods=['GET'])
def quote(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    lat1 = request.args.get('lat1', type=float)
    lon1 = request.args.get('lon1', type=float)
    lat2 = request.args.get('lat2', type=float)
    lon2 = request.args.get('lon2', type=float)

    if None in [lat1, lon1, lat2, lon2]:
        return jsonify(status='Error', message='Missing or invalid location parameters'), 400

    # Get the type of component and calculate the quote using the correct function
    component_type = component['type'].lower()  # Ensure the type is lowercase
    if component_type in quote_functions:
        quote_result = quote_functions[component_type](lat1, lon1, lat2, lon2, component_id)
    else:
        return jsonify(status='Error', message=f'No quote function available for component type: {component_type}'), 400

    return quote_result


@app.route('/components/<component_id>/request_delegation', methods=['POST'])
def request_delegation(component_id):
    component = components.get(component_id)
    if not component:
        return jsonify(status='Error', message='Component not found'), 404

    # Here you would implement the logic to handle the delegation request
    return jsonify(status='OK', delegation="Delegation result placeholder")


if __name__ == '__main__':
    app.run(port=5001)
