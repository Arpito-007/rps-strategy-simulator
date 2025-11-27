# data_handler.py
import json
import os
from datetime import datetime

class DataManager:

    def __init__(self, path="data/stats.json"):
        self.path = path
        self.stats = {"games": []}

        # ensure folder exists
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        # load if file exists
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    self.stats = json.load(f)
            except Exception:
                self.stats = {"games": []}

    def record_game(self, user, ai, result, predicted=None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
            "user": user,
            "ai": ai,
            "result": result,
            "predicted": predicted
        }
        self.stats["games"].append(entry)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.stats, f, indent=2)

    def get_games(self):
        return self.stats.get("games", [])


