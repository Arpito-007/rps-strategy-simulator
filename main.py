from game_utils import get_user_move, get_winner

def main():
    print("=== RPS Strategy Simulator ===")
    print("Day 1 Setup: Basic CLI Running\n")

    while True:
        user_move = get_user_move()
        if user_move == "exit":
            print("Exiting game...")
            break

        # AI TEMP: random for now (will be replaced later)
        import random
        ai_move = random.choice(["rock", "paper", "scissors"])

        print(f"AI played: {ai_move}")

        winner = get_winner(user_move, ai_move)
        print(winner)
        print("-" * 30)

if __name__ == "__main__":
    main()
