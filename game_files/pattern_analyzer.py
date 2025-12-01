# pattern_analyzer.py

class PatternAnalyzer:
    #Stores user's move history and returns recent patterns.
    
    def __init__(self, memory_size=10):
        self.history = []
        self.memory_size = memory_size

    def add_move(self, move):
        self.history.append(move)

    def recent(self, n=None):
        #Return the last n moves (or memory_size by default).
        if n is None:
            n = self.memory_size
        return self.history[-n:]

