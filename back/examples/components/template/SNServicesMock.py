import random
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.loggerConfig import get_configured_logger
import json
import os
import atexit
import requests as http_requests

class ComponentTemplate():

    def __init__(self, name, port=5000):
        self.logger = get_configured_logger()
        self.app = Flask(name) # Create a Flask app
        CORS(self.app)
        self.configure_routes()
        self.name = name
        self.port = port
        self.availability = "available"
        self.registered_tasks = []
        self.write_info()
        atexit.register(self.remove_info)

    # Register the component information in a JSON file so the Support Network Manager can find it
    def write_info(self):
        service_info = {
            'name': self.name,
            'port': self.port,
        }
        if os.path.exists('service_info.json'):
            with open('service_info.json', 'r') as f:
                existing_services = json.load(f)
        else:
            existing_services = []
        existing_services.append(service_info)
        with open('service_info.json', 'w') as f:
            json.dump(existing_services, f)

    # Remove the component information in a JSON file so the Support Network Manager can find only the available services
    def remove_info(self):
        if os.path.exists('service_info.json'):
            with open('service_info.json', 'r') as f:
                existing_services = json.load(f)

            existing_services = [service for service in existing_services if service['name'] != self.name]

            with open('service_info.json', 'w') as f:
                json.dump(existing_services, f)

    def configure_routes(self):

        @self.app.route('/health', methods=['GET'])
        def health():
            self.logger.info("Health check performed. App name: " + self.app.name)
            return jsonify(status='OK')

        @self.app.route('/status', methods=['GET'])
        def status():
            self.logger.info("Health check performed. App name: " + self.app.name)
            return jsonify(status=self.availability)
        
        @self.app.route('/info', methods=['GET'])
        def info():
            component_info = {
                "name": self.name,
                "port": self.port,
                "availability": self.availability,
                "registered_tasks": self.registered_tasks
            }
            return jsonify(status='OK', component=component_info)
        
        @self.app.route('/update_info', methods=['PUT'])
        def update_info():
            data = request.get_json()
            if 'name' in data:
                self.name = data['name']
            if 'availability' in data:
                self.availability = data['availability']
            if 'registered_tasks' in data:
                self.registered_tasks = data['registered_tasks']
            return jsonify(status='OK', message='Component information updated successfully')

        @self.app.route('/register_tasks', methods=['POST'])
        def register_tasks():
            tasks = request.get_json()
            self.registered_tasks = tasks
            registered_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Prepare the data for the API call
            component_info = {'port': self.port, 'name': self.name}
            tasks_data = [{'id': task['id'], 'registered_components': [component_info]} for task in tasks]

            # Assuming the task management API is at this URL and supports bulk update
            url = 'http://127.0.0.1:5000/tasks/bulk_update'
            response = http_requests.put(url, json=tasks_data)

            # Check if the request was successful
            if response.status_code != 200:
                return jsonify(status='ERROR', message='Failed to update tasks in the task management API')

            return jsonify(status='OK', registered_time=registered_time, message='Tasks registered successfully')

        @self.app.route('/remove_task', methods=['DELETE'])
        def remove_task():
            task_id = request.get_json().get('id')
            task_to_remove = None
            for task in self.registered_tasks:
                if task.get('id') == task_id:
                    task_to_remove = task
                    break
            if task_to_remove:
                self.registered_tasks.remove(task_to_remove)
                return jsonify(status='OK', message=f'Task with id {task_id} removed successfully.')
            else:
                return jsonify(status='Error', message=f'Task with id {task_id} not found.')

        # @self.app.route('/estimate', methods=['GET'])
        def estimate():
            #TODO: Implement estimate logic
            pass
        
        @self.app.route('/request_delegation', methods=['POST'])
        def request_delegation():
            #TODO: Implement request logic
            pass

        @self.app.route('/randomize', methods=['GET'])
        def randomize():
            self.availability = random.choice(["available", "unavailable"])
            return jsonify(status=self.availability)

    def run(self):
        # log_thread = threading.Thread(target=self.send_logs, daemon=True) # Daemonize the thread
        # log_thread.start()  
        self.app.run(port=self.port)

# Start the Flask app
if __name__ == '__main__':
    api = ComponentTemplate("Component Example", port=5002)
    api.run()

