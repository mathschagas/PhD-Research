import math
import time

class Actor:
    def __init__(self, id, start_x, start_y, speed_kmh):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.speed_kmh = speed_kmh  # Speed in km/h
        self.total_distance = 0
        self.distance_traveled = 0
        self.start_time = time.time()

    def move_towards(self, target_x, target_y, time_interval):
        previous_x, previous_y = self.x, self.y

        # Calculate the distance to move in this iteration based on speed and time interval
        distance_to_move = (self.speed_kmh / 3600) * time_interval  # Convert speed to km/s and multiply by time interval

        # Calculate the direction vector towards the target
        distance_to_target = self.calculate_distance(self.x, self.y, target_x, target_y)

        # Check if the actor is close enough to the destination to stop
        if distance_to_target <= distance_to_move:
            # Move directly to the destination and stop
            self.x = target_x
            self.y = target_y
            print(f"Actor {self.id} reached target location ({self.x:.6f}, {self.y:.6f})\n")
            return True  # Indicates that the actor has reached the destination

        # Otherwise, move normally towards the destination
        ratio = distance_to_move / distance_to_target if distance_to_target != 0 else 0
        self.x += ratio * (target_x - self.x)
        self.y += ratio * (target_y - self.y)

        # Calculate the distance moved in this iteration
        distance_moved = self.calculate_distance(previous_x, previous_y, self.x, self.y)
        self.distance_traveled += distance_moved

        elapsed_time = time.time() - self.start_time
        eta = self.estimated_time_to_arrival(target_x, target_y)

        print(f"Actor {self.id} moved to ({self.x:.6f}, {self.y:.6f})")
        print(f"Delivery time so far: {elapsed_time*time_interval:.2f} seconds")
        print(f"Estimated time to delivery: {eta:.2f} seconds")
        print(f"Distance traveled so far: {self.distance_traveled:.6f} km")
        print(f"Distance to destination: {distance_to_target:.6f} km")
        print(f"Total route distance: {self.total_distance:.6f} km")
        print(f"Actor's speed: {self.speed_kmh:.2f} km/h\n")
        return False  # Indicates that the actor has not reached the destination

    def estimated_time_to_arrival(self, target_x, target_y):
        remaining_distance = self.calculate_distance(self.x, self.y, target_x, target_y)
        if self.speed_kmh > 0:
            # Estimate time to arrival in hours and convert to seconds
            return (remaining_distance / self.speed_kmh) * 3600
        else:
            return float('inf')  # In case the actor isn't moving
