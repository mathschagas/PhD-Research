class UncertaintyMonitor:
    def __init__(self):
        self.conditions = {
            "internal_failure_drone": False,
            "internal_failure_car": False,
            "bad_weather": False,
            "restricted_area": False,
            "traffic_jam": False
        }
        self.current_actor = None

    def set_actor(self, actor_type):
        self.current_actor = actor_type
        # TODO: set the relevant conditions based on the actor type
        for key in self.conditions.keys():
            self.conditions[key] = False

    def force_uncertainty(self, uncertainty):
        # Force the specified uncertainty to occur
        for key in self.conditions.keys():
            self.conditions[key] = False
        self.conditions[uncertainty] = True

    def report(self, lat, lon):
        print(f"\nCurrent Conditions for {self.current_actor}:")
        # TODO: randomize chances of each condition that affects the actor
        for condition, state in self.conditions.items():
            if state:
                print(f"  {condition}: Yes")
        if any(self.conditions.values()):
            print(f"Problem detected at: ({lat:.6f}, {lon:.6f})")
        print()
