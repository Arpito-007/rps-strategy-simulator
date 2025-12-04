from flask import Flask, render_template, request, redirect, url_for
from ai_engine import AIPredictor
from pattern_analyzer import PatternAnalyzer
from data_handler import DataManager

app = Flask(__name__, template_folder="templates", static_folder="static")

# core objects
difficulty = "medium"
ai = AIPredictor(memory_size=20)
analyzer = PatternAnalyzer(memory_size=20)
dm = DataManager("data/stats.json")

dm.clear_games()
analyzer.history.clear()

# preload history if any
for g in dm.get_games():
    if "user" in g:
        analyzer.add_move(g["user"])

@app.route("/")
def index():
    return render_template("index.html", difficulty=difficulty)

@app.route("/play", methods=["POST"])
def play():
    user_move = request.form.get("move")
    if user_move not in ("rock", "paper", "scissors"):
        return redirect(url_for("index"))

    # AI move + predicted next move
    ai_move, predicted = ai.make_move(analyzer.history, difficulty=difficulty)

    # determine winner
    result = ai.determine_winner(user_move, ai_move)

    # update analyzer + save stats
    analyzer.add_move(user_move)
    dm.record_game(user_move, ai_move, result, predicted)
    dm.save()

    # return result page
    return render_template(
        "result.html",
        user_move=user_move,
        ai_move=ai_move,
        predicted=predicted,
        result=result,
        difficulty=difficulty
    )

@app.route("/change_difficulty", methods=["GET", "POST"])
def change_difficulty():
    global difficulty
    if request.method == "POST":
        new = request.form.get("difficulty")
        if new in ("easy", "medium", "hard"):
            difficulty = new
        return redirect(url_for("index"))
    return render_template("change_difficulty.html", current=difficulty)

@app.route("/scoreboard")
def scoreboard():
    games = dm.get_games()

    user_wins = sum(1 for g in games if g.get("result") == "user")
    ai_wins = sum(1 for g in games if g.get("result") == "ai")
    draws = sum(1 for g in games if g.get("result") == "draw")

    return render_template(
        "scoreboard.html",
        games=games,
        user_wins=user_wins,
        ai_wins=ai_wins,
        draws=draws
    )

@app.route("/reset_scoreboard", methods=["POST"])
def reset_scoreboard():
    dm.clear_games()
    # also clear the analyzer history so AI starts fresh
    analyzer.history.clear()
    return redirect(url_for("scoreboard"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


