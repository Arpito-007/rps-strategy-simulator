import numpy as np

class AIPredictor:
    def __init__(self):
        self.moves = ["rock", "paper", "scissors"]

    def predict(self, history):
        if not history:
            return np.random.choice(self.moves)

        counts = {m: history.count(m) for m in self.moves}
        probs = np.array(list(counts.values())) / sum(counts.values())

        return np.random.choice(self.moves, p=probs)

    def counter_move(self, predicted):
        counters = {
            "rock": "paper",
            "paper": "scissors",
            "scissors": "rock"
        }
        return counters[predicted]

    def determine_winner(self, user, ai):
        if user == ai:
            return "draw"
        if (user == "rock" and ai == "scissors") or \
           (user == "scissors" and ai == "paper") or \
           (user == "paper" and ai == "rock"):
            return "user"
        return "ai"
