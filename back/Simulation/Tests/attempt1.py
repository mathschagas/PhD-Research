import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drone Delivery Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Drone class
class Drone:
    def __init__(self, id, x, y, speed, reliability):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.reliability = reliability
        self.color = BLUE if reliability > 0.85 else GREEN if reliability > 0.75 else RED

    def move_towards(self, target_x, target_y):
        if self.x < target_x:
            self.x += self.speed
        elif self.x > target_x:
            self.x -= self.speed
        if self.y < target_y:
            self.y += self.speed
        elif self.y > target_y:
            self.y -= self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

# Observer class
class Observer:
    def __init__(self):
        self.conditions = {
            "sensor_failure": False,
            "bad_weather": False,
            "restricted_airspace": False
        }

    def detect_uncertainties(self):
        # Randomly activate uncertainties
        self.conditions["sensor_failure"] = random.choice([True, False])
        self.conditions["bad_weather"] = random.choice([True, False])
        self.conditions["restricted_airspace"] = random.choice([True, False])

    def report(self):
        print("Current Conditions:")
        for condition, state in self.conditions.items():
            print(f" - {condition}: {'Detected' if state else 'Normal'}")

# Simulation parameters
target_x, target_y = WIDTH // 2, HEIGHT // 2
drones = [
    Drone(id=1, x=random.randint(50, 750), y=random.randint(50, 550), speed=2, reliability=0.9),
    Drone(id=2, x=random.randint(50, 750), y=random.randint(50, 550), speed=2, reliability=0.8),
    Drone(id=3, x=random.randint(50, 750), y=random.randint(50, 550), speed=2, reliability=0.65)
]
observer = Observer()

# Main simulation loop
running = True
while running:
    screen.fill(WHITE)
    
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    except Exception as e:
        print(f"An error occurred: {e}")

    # Detect and report uncertainties
    observer.detect_uncertainties()
    observer.report()

    for drone in drones:
        if observer.conditions["bad_weather"] and random.random() < 0.7:
            print(f"Drone {drone.id} cannot proceed due to bad weather.")
        elif observer.conditions["restricted_airspace"] and random.random() < 0.5:
            print(f"Drone {drone.id} cannot proceed due to restricted airspace.")
        elif observer.conditions["sensor_failure"] and random.random() < 0.8:
            print(f"Drone {drone.id} experienced sensor failure.")
        else:
            drone.move_towards(target_x, target_y)

        drone.draw(screen)
    
    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()