from flask import Flask, render_template, request, redirect, url_for
from ai_engine import AIPredictor
from pattern_analyzer import PatternAnalyzer
from data_handler import DataManager

# ------------------ Flask app setup ------------------

app = Flask(__name__, template_folder="templates", static_folder="static")

if __name__ == "__main__":
    app.run()


# ------------------ Core objects ------------------

difficulty = "medium"  # default difficulty

ai = AIPredictor(memory_size=20)
analyzer = PatternAnalyzer(memory_size=20)
dm = DataManager("data/stats.json")

# If you want a fresh scoreboard + AI each time you start the server,
# keep these two lines. If you want persistence across runs, comment them out.
dm.clear_games()
analyzer.history.clear()

# Preload history if any (after clear_games this will usually be empty)
for g in dm.get_games():
    if "user" in g:
        analyzer.add_move(g["user"])

# ------------------ Routes ------------------

@app.route("/")
def intro():
    """Splash / landing page."""
    return render_template("intro.html")


@app.route("/game")
def index():
    """Main game UI page."""
    return render_template("index.html", difficulty=difficulty)



@app.route("/game")
def game():
    """Backward-compat: any url_for('game') just shows main page."""
    return redirect(url_for("index"))



@app.route("/play", methods=["POST"])
def play():
    """Handles a single round of the game."""
    user_move = request.form.get("move")

    # allow timeout move "none" as well
    if user_move not in ("rock", "paper", "scissors", "none"):
        return redirect(url_for("index"))

    # AI move + predicted next move
    ai_move, predicted = ai.make_move(analyzer.history, difficulty=difficulty)

    # determine winner
    result = ai.determine_winner(user_move, ai_move)

    # only learn from real moves, not "none"
    if user_move in ("rock", "paper", "scissors"):
        analyzer.add_move(user_move)

    # store game in JSON
    dm.record_game(user_move, ai_move, result, predicted)
    dm.save()

    # session stats for result screen
    games = dm.get_games()
    user_wins = sum(1 for g in games if g.get("result") == "user")
    ai_wins = sum(1 for g in games if g.get("result") == "ai")
    draws = sum(1 for g in games if g.get("result") == "draw")
    total_rounds = len(games)
    prediction_correct = (predicted == user_move)

    return render_template(
        "result.html",
        user_move=user_move,
        ai_move=ai_move,
        predicted=predicted,
        result=result,
        difficulty=difficulty,
        user_wins=user_wins,
        ai_wins=ai_wins,
        draws=draws,
        total_rounds=total_rounds,
        prediction_correct=prediction_correct,
    )


@app.route("/change_difficulty", methods=["GET", "POST"])
def change_difficulty():
    """Page to switch between Easy / Medium / Hard."""
    global difficulty

    if request.method == "POST":
        new = request.form.get("difficulty")
        if new in ("easy", "medium", "hard"):
            difficulty = new
        # whatever happens, go back to main game page
        return redirect(url_for("index"))

    # GET request: just show the page with current difficulty
    return render_template("change_difficulty.html", current=difficulty)


@app.route("/scoreboard")
def scoreboard():
    """Show stats from all games stored in JSON."""
    games = dm.get_games()

    user_wins = sum(1 for g in games if g.get("result") == "user")
    ai_wins = sum(1 for g in games if g.get("result") == "ai")
    draws = sum(1 for g in games if g.get("result") == "draw")

    return render_template(
        "scoreboard.html",
        games=games,
        user_wins=user_wins,
        ai_wins=ai_wins,
        draws=draws,
    )


@app.route("/reset_scoreboard", methods=["POST"])
def reset_scoreboard():
    """Clear JSON stats + AI history."""
    dm.clear_games()
    analyzer.history.clear()
    return redirect(url_for("scoreboard"))


# ------------------ Run server ------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)