# server.py
from flask import Flask, render_template, request, jsonify
from ai_engine import AIPredictor
from pattern_analyzer import PatternAnalyzer
from data_handler import DataManager

app = Flask(__name__, static_folder="static", template_folder="templates")

# global state
difficulty = "medium"
ai = AIPredictor(memory_size=20)
analyzer = PatternAnalyzer(memory_size=20)
dm = DataManager("data/stats.json")

# preload history
for g in dm.get_games():
    if "user" in g:
        analyzer.add_move(g["user"])

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/play")
def play():
    data = request.get_json(force=True)
    user_move = data.get("user_move")
    if user_move not in ("rock","paper","scissors"):
        return jsonify({"error": "invalid move"}), 400

    ai_move, predicted = ai.make_move(analyzer.history, difficulty=difficulty)
    result = ai.determine_winner(user_move, ai_move)

    analyzer.add_move(user_move)
    dm.record_game(user_move, ai_move, result)
    dm.save()

    return jsonify({"ai_move": ai_move, "predicted": predicted, "result": result})

@app.post("/set_difficulty")
def set_difficulty():
    global difficulty
    data = request.get_json(force=True)
    level = data.get("level")
    if level not in ("easy","medium","hard"):
        return jsonify({"error":"invalid difficulty"}), 400
    difficulty = level
    return jsonify({"status":"ok","difficulty":difficulty})

@app.get("/stats")
def stats():
    games = dm.get_all_games()
    user_wins = sum(1 for g in games if g.get("result") == "user")
    ai_wins = sum(1 for g in games if g.get("result") == "ai")
    draws = sum(1 for g in games if g.get("result") == "draw")
    return jsonify({"total": len(games), "user_wins": user_wins, "ai_wins": ai_wins, "draws": draws})

if __name__ == "__main__":
    app.run(debug=True)
