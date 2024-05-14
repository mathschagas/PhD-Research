import json
import random
import colorlog
import logging
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

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

initial_data = {
    # "availability": "available",  # "available" or "unavailable
    # "price": 100.0,
    # "speed": 50.0,
    # "time_to_finish": 20.0
}

class SNComponentAPI:
    def __init__(self, name):
        self.app = Flask(name) # Create a Flask app
        CORS(self.app)
        self.configure_routes()
        self.data = initial_data

    def configure_routes(self):
        @self.app.route('/health')
        def health():
            logger.info("Health check performed. App name: " + self.app.name)
            return jsonify(status='OK')

        @self.app.route('/get_data', methods=['GET'])
        def get_data():
            logger.info("Retrieving data from Support Network Component: " + json.dumps(self.data))
            return jsonify(self.data)

        @self.app.route('/update_data', methods=['PUT'])
        def update_data():
            self.data.update(request.json)
            logger.info("Updating data from Support Network Component: " + json.dumps(self.data))
            return jsonify(self.data)

        @self.app.route('/update_random_data', methods=['GET'])
        def update_random_data():
            self.data["availability"] = random.choice(["available", "unavailable"])
            self.data["price"] = random.uniform(1, 100)
            self.data["speed"] = random.uniform(1, 100)
            self.data["time_to_finish"] = random.uniform(1, 100)
            logger.info("Randomizing data from Support Network Component: " + json.dumps(self.data))
            return jsonify(self.data)
        
    # Function to send logs every 10 seconds
    def send_logs(self):
        while True:
            time.sleep(5)  # Log every 10 seconds
            logger.info("SNComponent (" + self.app.name + ") is running. Current data: " + json.dumps(self.data))

    def run(self, port=5000):
        log_thread = threading.Thread(target=self.send_logs, daemon=True) # Daemonize the thread
        log_thread.start()  
        self.app.run(port=port)

# Start the Flask app
if __name__ == '__main__':
    api = SNComponentAPI("SNC Example")
    api.run()