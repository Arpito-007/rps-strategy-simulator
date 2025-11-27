from ai_engine import AIPredictor
from data_handler import DataManager
from analyzer import PatternAnalyzer
from visualization import Visualizer

def get_user_move():
    move = input("Enter move (rock/paper/scissors or q to quit): ").lower()
    if move in ["rock", "paper", "scissors"]:
        return move
    elif move == "q":
        return None
    else:
        print("Invalid move. Try again.")
        return get_user_move()

def main():
    dm = DataManager("data/stats.json")
    analyzer = PatternAnalyzer()
    ai = AIPredictor()
    visual = Visualizer()

    print("\n=== Strategy-Analyzing RPS Simulator ===\n")

    while True:
        user = get_user_move()
        if user is None:
            break

        analyzer.add_move(user)
        predicted_player_move = ai.predict(analyzer.recent_pattern())
        ai_move = ai.counter_move(predicted_player_move)

        print(f"AI played: {ai_move}")

        result = ai.determine_winner(user, ai_move)
        print(f"Result: {result}\n")

        dm.record_game(user, ai_move, result)

    dm.save()
    visual.plot_stats(dm.stats)
    print("\nSession saved!")

if __name__ == "__main__":
    main()
