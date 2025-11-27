# main.py
from ai_engine import AIPredictor
from data_handler import DataManager
from pattern_analyzer import PatternAnalyzer

def choose_difficulty():
    print("Choose difficulty:")
    print("  1) Easy   (user has advantage)")
    print("  2) Medium (50/50)")
    print("  3) Hard   (AI uses strongest prediction)")
    choice = input("Enter 1, 2 or 3 (default 2): ").strip()
    if choice == "1":
        return "easy"
    if choice == "3":
        return "hard"
    return "medium"

def get_user_move():
    move = input("Enter move (rock/paper/scissors or q to quit): ").lower().strip()
    if move in ["rock", "paper", "scissors"]:
        return move
    if move == "q":
        return None
    print("Invalid input. Try again.")
    return get_user_move()

def main():
    print("\n=== Strategy-Analyzing RPS Simulator (CLI) ===\n")
    difficulty = choose_difficulty()
    print(f"Selected difficulty: {difficulty.upper()}\n")

    data_manager = DataManager("data/stats.json")
    analyzer = PatternAnalyzer(memory_size=20)
    ai = AIPredictor(memory_size=20)

    # preload history from saved games (so AI has more data across sessions)
    for g in data_manager.get_games():
        if "user" in g:
            analyzer.add_move(g["user"])

    total = 0
    user_wins = 0
    ai_wins = 0
    draws = 0

    while True:
        user_move = get_user_move()
        if user_move is None:
            break

        full_history = analyzer.history  # full history so predictor has max data
        ai_move, predicted = ai.make_move(full_history, difficulty=difficulty)
        result = ai.determine_winner(user_move, ai_move)

        analyzer.add_move(user_move)
        data_manager.record_game(user_move, ai_move, result)  # we keep storage minimal
        data_manager.save()

        total += 1
        if result == "user":
            user_wins += 1
            print(f"AI played: {ai_move}  -> You WIN this round!")
        elif result == "ai":
            ai_wins += 1
            print(f"AI played: {ai_move}  -> AI WINS this round.")
        else:
            draws += 1
            print(f"AI played: {ai_move}  -> It's a DRAW.")

        print(f"Predicted by AI: {predicted}")
        print(f"Score: You {user_wins}  |  AI {ai_wins}  |  Draws {draws}  |  Rounds {total}\n")

    print("\nSession ended. Results saved to data/stats.json")
    print(f"Final score - You: {user_wins}, AI: {ai_wins}, Draws: {draws}, Rounds: {total}\n")

if __name__ == "__main__":
    main()
