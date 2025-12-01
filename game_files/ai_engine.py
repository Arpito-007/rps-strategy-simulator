import random
from collections import defaultdict

class AIPredictor:
    """
    AI with three difficulty behaviors:
      - Easy: biased to lose (to favor user)
      - Medium: 50% predictive, 50% random
      - Hard: deterministic argmax prediction (strongest)
    """

    def __init__(self, memory_size=10):
        self.moves = ["rock", "paper", "scissors"]
        self.memory_size = memory_size

    # ---------- low-level helpers ----------
    def _random_move(self):
        return random.choice(self.moves)

    def _counter_of(self, move):
        counters = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
        return counters.get(move, self._random_move())

    def _losing_against(self, move):
        # return a move that loses to `move` (so the user would beat this move)
        losers = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        return losers.get(move, self._random_move())

    # ---------- prediction methods ----------
    def _freq_predict(self, history):
        """Predict the next player move using frequency (returns one move)."""
        if not history:
            return self._random_move()
        counts = {m: history.count(m) for m in self.moves}
        # choose the move with highest count (argmax)
        # if ties, random among top
        max_count = max(counts.values())
        top = [m for m, c in counts.items() if c == max_count]
        return random.choice(top)

    def _markov_predict(self, full_history, order=1):
        """Simple Markov-like predictor (returns one move)."""
        if not full_history:
            return self._random_move()

        # build conditional counts
        cond = defaultdict(lambda: defaultdict(int))
        for i in range(len(full_history) - order):
            key = tuple(full_history[i:i+order])
            nxt = full_history[i+order]
            cond[key][nxt] += 1

        last_key = tuple(full_history[-order:]) if len(full_history) >= order else None
        if last_key and last_key in cond and sum(cond[last_key].values()) > 0:
            counts = cond[last_key]
            max_count = max(counts.values())
            top = [m for m, c in counts.items() if c == max_count]
            return random.choice(top)

        # fallback to frequency argmax
        return self._freq_predict(full_history[-self.memory_size:])

    # ---------- public API ----------
    def predict_player_move(self, full_history, difficulty="medium"):
        """
        Returns the predicted next user move (single move string).
        difficulty controls which predictor is used later by make_move.
        """
        diff = (difficulty or "medium").lower()
        # For prediction we return a single best-guess (argmax) so countering is stronger.
        if diff == "hard":
            # try Markov order 2 then fallback to order 1 then freq
            if len(full_history) >= 2:
                return self._markov_predict(full_history, order=2)
            return self._markov_predict(full_history, order=1)
        # medium and easy use freq-prediction for consistency (but decision logic differs)
        return self._freq_predict(full_history[-self.memory_size:])

    def make_move(self, full_history, difficulty="medium"):
        """
        Returns a tuple: (ai_move, predicted_player_move)
        Behavior:
          - Easy: AI often picks a move that loses to predicted player move (user advantage)
          - Medium: 50% predictive-counter, 50% random
          - Hard: deterministic counter to argmax prediction (AI advantage)
        """
        diff = (difficulty or "medium").lower()
        predicted = self.predict_player_move(full_history, difficulty=diff)

        if diff == "easy":
            # Easy: mostly intentionally lose
            # Strategy:
            #  - 65% pick a move that loses to the predicted (so user likely wins)
            #  - 25% random (introduces noise)
            #  - 10% counter (surprise)
            r = random.random()
            if r < 0.65:
                # pick a move that loses to predicted -> user beats AI
                ai_move = self._losing_against(predicted)
            elif r < 0.9:
                ai_move = self._random_move()
            else:
                ai_move = self._counter_of(predicted)
            return ai_move, predicted

        if diff == "medium":
            # Medium: 50% deterministic counter, 50% random
            if random.random() < 0.5:
                ai_move = self._counter_of(predicted)
            else:
                ai_move = self._random_move()
            return ai_move, predicted

        # Hard (default): deterministic strong counter to predicted (argmax)
        # Use the strongest prediction (argmax) and always counter it.
        ai_move = self._counter_of(predicted)
        return ai_move, predicted

    def determine_winner(self, user, ai):
        if user == ai:
            return "draw"
        wins = {("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")}
        if (user, ai) in wins:
            return "user"
        return "ai"


