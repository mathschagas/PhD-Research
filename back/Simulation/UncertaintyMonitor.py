import random

chance_of_failure = 0.10

class UncertaintyMonitor:
    def __init__(self):
        self.conditions = {
            "bad_weather": False,
            "restricted_airspace": False,
            "sensor_failure": False,
            "traffic": False,
            "mechanical_issue": False
        }
        self.current_actor = None

    def set_actor(self, actor_type):
        self.current_actor = actor_type
        # Reset the relevant conditions
        if actor_type == "Drone1":
            self.conditions.update({
                "bad_weather": False,
                "restricted_airspace": False,
                "sensor_failure": False
            })
        elif actor_type == "Car1":
            self.conditions.update({
                "traffic": False,
                "mechanical_issue": False
            })

    def detect_uncertainties(self):
        # Simulate the random detection of uncertainties
        if self.current_actor == "Drone1":
            self.conditions["bad_weather"] = random.random() < chance_of_failure
            self.conditions["restricted_airspace"] = random.random() < chance_of_failure
            self.conditions["sensor_failure"] = random.random() < chance_of_failure
        elif self.current_actor == "Car1":
            self.conditions["traffic"] = random.random() < chance_of_failure
            self.conditions["mechanical_issue"] = random.random() < chance_of_failure

    def report(self, lat, lon):
        print(f"\nCurrent Conditions for {self.current_actor}:")
        for condition, state in self.conditions.items():
            if state:
                print(f"  {condition}: Yes")
        if any(self.conditions.values()):
            print(f"Problem detected at: ({lat:.6f}, {lon:.6f})")
        print()
