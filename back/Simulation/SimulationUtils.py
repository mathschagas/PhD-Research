import random
import math

# Define the bounding box for London (approximate latitude and longitude)
LONDON_BOUNDING_BOX = {
    "min_lat": 51.28,  # Southernmost point
    "max_lat": 51.70,  # Northernmost point
    "min_lon": -0.52,  # Westernmost point
    "max_lon": 0.33    # Easternmost point
}

def random_position_within_london():
    lat = random.uniform(LONDON_BOUNDING_BOX["min_lat"], LONDON_BOUNDING_BOX["max_lat"])
    lon = random.uniform(LONDON_BOUNDING_BOX["min_lon"], LONDON_BOUNDING_BOX["max_lon"])
    return lat, lon


# Function to generate a random position within a maximum distance of 30 km from the central point
def random_position_within_london_30km():
    # Define the central point of London (approximate latitude and longitude)
    central_london = (51.5074, -0.1278)  # Latitude and Longitude of London
    R = 6371  # Radius of the Earth in km
    # Generate a random distance in km up to the maximum allowed
    distance = random.uniform(5, 15) / R  # Convert the distance to radians
    # Generate a random angle
    angle = random.uniform(0, 2 * math.pi)
    # Latitude and Longitude of the central point in radians
    center_lat, center_lon = map(math.radians, central_london)
    # Calculate the new latitude and longitude
    new_lat = math.asin(math.sin(center_lat) * math.cos(distance) + 
                        math.cos(center_lat) * math.sin(distance) * math.cos(angle))
    new_lon = center_lon + math.atan2(math.sin(angle) * math.sin(distance) * math.cos(center_lat),
                                      math.cos(distance) - math.sin(center_lat) * math.sin(new_lat))
    # Convert back to degrees
    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)
    # Return the new position in latitude and longitude
    return new_lat, new_lon


def calculate_distance(x1, y1, x2, y2):
    # Using the Haversine formula for a more accurate distance calculation
    R = 6371  # Radius of the Earth in km
    lat1, lon1 = math.radians(x1), math.radians(y1)
    lat2, lon2 = math.radians(x2), math.radians(y2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
