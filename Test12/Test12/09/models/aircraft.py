class Aircraft:
    def __init__(self, type, speed, fuel_capacity):
        self.type = type
        self.speed = speed
        self.fuel_capacity = fuel_capacity

    def __str__(self):
        return f"Type: {self.type}, Speed: {self.speed}, Fuel Capacity: {self.fuel_capacity}"