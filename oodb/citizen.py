import json

class Citizen:
    def __init__(self, pan_number, name, dob, address):
        self.pan_number = pan_number
        self.name = name
        self.dob = dob
        self.address = address

    def to_dict(self):
        return {
            "pan_number": self.pan_number,
            "name": self.name,
            "dob": self.dob,
            "address": self.address
        }

    def __str__(self):
        return f"[{self.pan_number}] {self.name} ({self.dob}) - {self.address}"
