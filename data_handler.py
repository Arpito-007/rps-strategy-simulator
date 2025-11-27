import json
import os

class DataManager:
    def __init__(self, path):
        self.path = path
        self.stats = {"games": []}

        if os.path.exists(path):
            with open(path, "r") as f:
                self.stats = json.load(f)

    def record_game(self, user, ai, result):
        self.stats["games"].append({
            "user": user,
            "ai": ai,
            "result": result
        })

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.stats, f, indent=4)

