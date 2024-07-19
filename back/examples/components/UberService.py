import random
import sys
sys.path.insert(0, 'C:/Users/math_/Workspace/Doutorado/PhD-Research/back')

from flask import jsonify
from examples.components.template.ComponentTemplate import ComponentTemplate
from utils.lat_lon import calculate_haversine_distance, generate_random_position_london

class UberService(ComponentTemplate):

    def __init__(self, name, port):
        super().__init__(name, port)

    def configure_routes(self): # Override the configure_routes method
        super().configure_routes() # Call the parent class method

        @self.app.route('/estimate', methods=['GET'])
        def estimate_uber():
            speed = random.uniform(40, 60)  # Random speed between 40 and 60 km/h
            cost_per_km = random.uniform(0.8, 1.2)  # Random cost between 0.8 and 1.2 $/km

            lat1, lon1 = generate_random_position_london()
            lat2, lon2 = generate_random_position_london()
            distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)

            # Calculating time in hours and converting to minutes
            time_hours = distance / speed
            time_to_deliver = round(time_hours * 60, 2)
            
            # Calculating total cost
            price = round(distance * cost_per_km, 2)
            
            return jsonify(status="OK", cbr = { "time_to_deliver": time_to_deliver, "price": price })
        
        @self.app.route('/request_delegation', methods=['GET'])
        def request_delegation_uber(self):
            return jsonify(status='OK', message='Request delegation logic not implemented.')
        

if __name__ == '__main__':
    component = UberService("UberService", 5002)
    component.run()
