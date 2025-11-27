class PatternAnalyzer:
    def __init__(self, memory_size=5):
        self.history = []
        self.memory_size = memory_size

    def add_move(self, move):
        self.history.append(move)
        if len(self.history) > self.memory_size:
            self.history.pop(0)

    def recent_pattern(self):
        return self.history[-self.memory_size:]
