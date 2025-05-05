from flask import Flask, jsonify, request
from flask_cors import CORS
import json

class marketplace:
   
    def __init__(self, name):
    
        self.app = Flask(name) # Create a Flask app
        CORS(self.app, resources={r"/tasks/*": {"origins": "*"}})
        self.configure_routes()
        try:
            with open('constraintTasks.json', 'r') as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            print("File not found. Please ensure the file exists.")
            self.tasks = []
        except json.JSONDecodeError:
            print("File is empty. Starting with an empty task list.")
            self.tasks = []

    
    def configure_routes(self):

        @self.app.route('/tasks/', methods=['OPTIONS'])
        def options():
            return {}, 200

        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'OK'})

        @self.app.route('/tasks', methods=['GET'])
        def get_tasks():
            return jsonify(self.tasks)

        @self.app.route('/tasks', methods=['POST'])
        def create_task():
            task = request.get_json()
            self.tasks.append(task)
            return jsonify(task), 201
        
        @self.app.route('/tasks/bulk', methods=['POST'])
        def create_tasks():
            tasks = request.get_json()
            for task in tasks:
                self.tasks.append(task)
            return jsonify(tasks), 201

        @self.app.route('/tasks/<task_id>', methods=['GET'])
        def get_task(task_id):
            for task in self.tasks:
                if str(task['id']) == task_id:
                    return jsonify(task)
            return jsonify({'error': 'Task not found'}), 404

        @self.app.route('/tasks/bulk_update', methods=['PUT'])
        def update_tasks():
            updated_tasks = request.get_json()
            for updated_task in updated_tasks:
                for i, existing_task in enumerate(self.tasks):
                    if str(existing_task['id']) == str(updated_task['id']):
                        # Check if 'registered_components' is in updated_task
                        if 'registered_components' in updated_task:
                            # Check if 'registered_components' exists in self.tasks[i]
                            if 'registered_components' not in self.tasks[i]:
                                # Initialize it with an empty list if it doesn't exist
                                self.tasks[i]['registered_components'] = []
                            # Add to the existing list of registered components
                            self.tasks[i]['registered_components'].extend(updated_task['registered_components'])
                            # Remove 'registered_components' from updated_task to prevent it from overwriting the existing list
                            del updated_task['registered_components']
                        # Merge existing task with updated task
                        self.tasks[i].update(updated_task)
            return jsonify(self.tasks), 200

        @self.app.route('/tasks/<task_id>', methods=['PUT'])
        def update_task(task_id):
            task_data = request.get_json()
            for task in self.tasks:
                if str(task['id']) == task_id:
                    task.update(task_data)
                    print(task)
                    return jsonify(task)
            return jsonify({'error': 'Task not found'}), 404

        @self.app.route('/tasks/<task_id>', methods=['DELETE'])
        def delete_task(task_id):
            for task in self.tasks:
                if str(task['id']) == task_id:
                    self.tasks.remove(task)
                    return jsonify({'message': 'Task deleted'})
            return jsonify({'error': 'Task not found'}), 404
    

    def run(self, port=5000):
        self.app.run(port=port)


# Start the Flask app
if __name__ == '__main__':
    api = marketplace("Marketplace")
    api.run()