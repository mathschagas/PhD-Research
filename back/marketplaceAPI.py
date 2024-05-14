from flask import Flask, jsonify, request
from flask_cors import CORS

tasks = []

class marketplaceAPI:
    def __init__(self, name):
        self.app = Flask(name) # Create a Flask app
        CORS(self.app, resources={r"/tasks/*": {"origins": "*"}})

        self.configure_routes()
        self.data = tasks

    def configure_routes(self):

        @self.app.route('/tasks/', methods=['OPTIONS'])
        def options():
            return {}, 200

        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'OK'})

        @self.app.route('/tasks', methods=['GET'])
        def get_tasks():
            return jsonify(tasks)

        @self.app.route('/tasks', methods=['POST'])
        def create_task():
            task = request.get_json()
            tasks.append(task)
            return jsonify(task), 201

        @self.app.route('/tasks/<int:task_id>', methods=['GET'])
        def get_task(task_id):
            for task in tasks:
                if task['id'] == task_id:
                    return jsonify(task)
            return jsonify({'error': 'Task not found'}), 404

        @self.app.route('/tasks/<int:task_id>', methods=['PUT'])
        def update_task(task_id):
            task_data = request.get_json()
            for task in tasks:
                if task['id'] == task_id:
                    task.update(task_data)
                    return jsonify(task)
            return jsonify({'error': 'Task not found'}), 404

        @self.app.route('/tasks/<int:task_id>', methods=['DELETE'])
        def delete_task(task_id):
            for task in tasks:
                if task['id'] == task_id:
                    tasks.remove(task)
                    return jsonify({'message': 'Task deleted'})
            return jsonify({'error': 'Task not found'}), 404
    
    def run(self, port=5001):
        self.app.run(port=port)


# Start the Flask app
if __name__ == '__main__':
    api = marketplaceAPI("Marketplace Example")
    api.run()