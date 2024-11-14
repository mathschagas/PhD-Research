from itertools import permutations

def get_permutations(component_types = None):
    ct = []
    if component_types is None:
        ct = ["drone", "car", "bicycle", "truck", "pedestrian"]
    else:
        ct = component_types
    # Generate all permutations starting with "drone"
    drone_permutations = [["drone"] + list(perm) for i in range(len(ct)) for perm in permutations(ct[1:], i)]
    # Generate all permutations starting with "car"
    car_permutations = [["car"] + list(perm) for i in range(len(ct)) for perm in permutations(ct[0:1] + ct[2:], i)]
    # Combine both lists
    all_permutations = drone_permutations + car_permutations
    # Create the result dictionary
    result = {i + 1: perm for i, perm in enumerate(all_permutations)}
    return result
