import json
import colorlog
import logging
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

from decision_making import calculate_delegation_cbr_score

# Configure colorlog for colored logs
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(levelname)s] [%(asctime)s] %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'white',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    datefmt='%Y/%m/%d %H:%M:%S'  # Format of %(asctime)s
))
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class SupportNetworkManager:
    def __init__(self, name):
        self.app = Flask(name) # Create a Flask app
        CORS(self.app)
        self.configure_routes()
        self.data = []
        self.update_data()

    def update_data(self):
        with open('service_info.json', 'r') as f:
            file_data = json.load(f)
    
        file_data_ports = {service['port'] for service in file_data}
        self_data_ports = {service['port'] for service in self.data}
    
        # Remove services from self.data that are not in the file
        self.data = [service for service in self.data if service['port'] in file_data_ports]
    
        # Add services to self.data that are in the file but not in self.data
        for service in file_data:
            if service['port'] not in self_data_ports:
                self.data.append(service)

        self.load_services_data()

    def load_services_data(self):
        for i in range(len(self.data)):
            response = requests.get(f'http://localhost:{self.data[i]["port"]}/info')
            self.data[i] = response.json()['component']
    
    def configure_routes(self):

        @self.app.route('/health')
        def health():
            logger.info("Health check performed. App name: " + self.app.name)
            return jsonify(status='OK')

        @self.app.route('/get_data', methods=['GET'])
        def get_data():
            self.update_data()
            logger.info("Retrieving data from Support Network Component: " + json.dumps(self.data))
            return jsonify(self.data)
        
        @self.app.route('/request_delegation/<selectedTask>/<selectedScenario>', methods=['GET'])
        def decision_making(selectedTask, selectedScenario):
            task = {'id': selectedTask, 'scenario': selectedScenario}
            score = calculate_delegation_cbr_score(task)
            return jsonify(score)

    # Function to send logs every 10 seconds
    def send_update_logs(self):
        while True:
            time.sleep(10)  # Log every 10 seconds
            # self.update_data()
            logger.info("SNComponent (" + self.app.name + ") is running. Current data: " + json.dumps(self.data))

    def run(self, port=5001):
        log_thread = threading.Thread(target=self.send_update_logs, daemon=True) # Daemonize the thread
        log_thread.start()  
        self.app.run(port=port)

# Start the Flask app
if __name__ == '__main__':
    api = SupportNetworkManager("SupportNetwork Manager")
    api.run()