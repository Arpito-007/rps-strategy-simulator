def get_user_move():
    move = input("Enter your move (rock/paper/scissors or exit): ").lower().strip()

    valid = ["rock", "paper", "scissors", "exit"]
    if move not in valid:
        print("Invalid move! Try again.")
        return get_user_move()

    return move


def get_winner(player, ai):
    if player == ai:
        return "It's a draw!"

    rules = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    if rules[player] == ai:
        return "You win!"
    else:
        return "AI wins!"
