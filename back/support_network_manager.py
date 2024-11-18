import json
import colorlog
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

from decision_making import calculate_delegation_cbr_score

# Create a session
session = requests.Session()

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


# Configure colorlog for colored logs
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(asctime)s] %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'white',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    datefmt='%Y/%m/%d %H:%M:%S'
))
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class SupportNetworkManager:
    def __init__(self, name):
        self.app = Flask(name)
        CORS(self.app)
        self.configure_routes()
        self.data = []
        self.mock_api_url = 'http://localhost:5001/components/all'  # Mock API URL
        self.update_data()

    def update_data(self):
        # Update data from local components
        self.update_local_components()
        # Update data from mock API components
        self.update_mock_components()

    def update_local_components(self):
        try:
            with open('service_info.json', 'r') as f:
                file_data = json.load(f)
            file_data_ports = {service['id'] for service in file_data}
            self_data_ports = {service['id'] for service in self.data}

            # Remove services from self.data that are not in the file
            self.data = [service for service in self.data if service['port'] in file_data_ports]

            # Add services to self.data that     are in the file but not in self.data
            for service in file_data:
                if service['port'] not in self_data_ports:
                    response = session.get(f'http://localhost:{service["port"]}/info')
                    if response.status_code == 200:
                        self.data.append(response.json()['component'])

            logger.info(f"Local components loaded: {len(self.data)} components")
        except FileNotFoundError:
            logger.warning("service_info.json not found. No local components loaded.")
        except requests.RequestException as e:
            logger.error(f"Failed to connect to local API: {e}")

    def update_mock_components(self):
        try:
            response = session.get(self.mock_api_url)
            if response.status_code == 200:
                mock_components = response.json().get('components', [])
                self.data = mock_components  # Update mock components in the components list
                logger.info(f"Mock components loaded: {len(mock_components)} components")
            else:
                logger.warning(f"Failed to retrieve mock components: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to connect to mock API at {self.mock_api_url}: {e}")

    def configure_routes(self):

        @self.app.route('/health')
        def health():
            logger.info("Health check performed. App name: " + self.app.name)
            return jsonify(status='OK')

        @self.app.route('/get_data', methods=['GET'])
        def get_data():
            self.update_data()
            logger.info("Retrieving data from Support Network Components: " + json.dumps(self.data))
            return jsonify(self.data)
        
        @self.app.route('/request_delegation/<selectedTask>/<selectedScenario>', methods=['GET'])
        def decision_making(selectedTask, selectedScenario):
            # Get the latitude and longitude from the query string
            lat1 = request.args.get('lat1')
            lon1 = request.args.get('lon1')
            lat2 = request.args.get('lat2')
            lon2 = request.args.get('lon2')
            uncertainty = request.args.get('uncertainty')

            task = {
                'id': selectedTask,
                'scenario': selectedScenario,
                'uncertainty': uncertainty,
                'start_location': {'lat': lat1, 'lon': lon1},
                'end_location': {'lat': lat2, 'lon': lon2}
            }

            score = calculate_delegation_cbr_score(task, uncertainty)
            return jsonify(score)
        
    # Function to send logs every 10 seconds
    # def send_update_logs(self):
        # while True:
            # time.sleep(10)
            # logger.info("SNComponent (" + self.app.name + ") is running. Current data: " + json.dumps(self.data))

    def run(self, port=5002):
        # log_thread = threading.Thread(target=self.send_update_logs, daemon=True)
        # log_thread.start()  
        self.app.run(port=port)

# Start the Flask app
if __name__ == '__main__':
    api = SupportNetworkManager("SupportNetwork Manager")
    api.run()
