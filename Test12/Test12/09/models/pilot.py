class Pilot:

    def __init__(self, name, skill):
        self.name = name
        self.skill = skill

    def __str__(self):
        return f"Pilot: [name: {self.name}, skill: {self.skill}] "