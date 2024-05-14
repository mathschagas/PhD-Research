import colorlog
from flask import Flask, jsonify
import requests
import logging
import json

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


app = Flask("SNM")

SN_COMPONENT_API_URL = 'http://localhost:5000'  # URL of the SNComponentAPI service

@app.route('/health')
def health():
    logger.info("Health check performed. App name: " + app.name)
    return jsonify(status='OK')

@app.route('/get_data', methods=['GET'])
def get_data():
    response = requests.get(SN_COMPONENT_API_URL + '/get_data')
    data = response.json()
    app.logger.info("Retrieved data from Support Network Component: " + json.dumps(data))
    return jsonify(data)

@app.route('/update_data', methods=['PUT'])
def update_data():
    new_data = {"price": 50.0, "speed": 25.0, "time_to_finish": 10.0}  # This should be the new data you want to update
    response = requests.put(SN_COMPONENT_API_URL + '/update_data', json=new_data)
    data = response.json()
    app.logger.info("Updated data in Support Network Component: " + json.dumps(data))
    return jsonify(data)

@app.route('/update_random_data', methods=['PUT'])
def update_random_data():
    response = requests.put(SN_COMPONENT_API_URL + '/update_random_data')
    data = response.json()
    app.logger.info("Randomized data in Support Network Component: " + json.dumps(data))
    return jsonify(data)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(port=5001)  # Run this service on a different port