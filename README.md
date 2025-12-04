# rps-strategy-simulator
🧠 AI-Based Rock-Paper-Scissors Strategy Simulator

A modern, interactive Rock-Paper-Scissors game built with Flask, featuring:

Adaptive AI that learns player patterns

Multiple difficulty levels (Easy / Medium / Hard)

Real-time timer system

Beautiful animated UI

Scoreboard tracking and game history

Responsive layout + polished aesthetics

This project was created as part of a school/college assessment demonstrating Python backend logic, pattern recognition, machine learning basics, and frontend design skills.

🚀 Features
🎮 Three Difficulty Modes

Easy: AI intentionally loses most of the time

Medium: AI mixes prediction & randomness

Hard: AI predicts player moves using frequency & Markov chains

⏳ 40-Second Timer

Player must choose within 40 seconds

If time runs out → system auto-submits "none"

AI always wins on timeout

Timer animation turns red & shakes in final 5 seconds

📊 Scoreboard

Tracks:

User wins

AI wins

Draws

Total rounds

AI prediction accuracy

💾 Persistent Game History

Game results are stored in a local JSON file and displayed in the scoreboard.

🎨 Beautiful Aesthetic UI

Smooth intro animation

Hover motions, button transitions

Centered clean layout

Works on desktop + mobile

🧩 Project Structure
rps-strategy-simulator/
│
├── server.py              # Flask backend
├── ai_engine.py           # AI prediction logic
├── pattern_analyzer.py    # Pattern memory system
├── data_handler.py        # JSON data saving/loading
│
├── data/
│   └── stats.json         # Scoreboard database
│
├── static/
│   ├── style.css          # Full website styling/animations
│   └── icons/             # Rock, Paper, Scissors icons
│
└── templates/
    ├── intro.html         # Intro splash screen
    ├── index.html         # Main gameplay page
    ├── result.html        # Score display after each round
    ├── scoreboard.html    # Full scoreboard history
    └── change_difficulty.html

⚙️ How the AI Works
🧠 AIPredictor

The AI uses 3 strategies:

Easy Mode

65% chance to intentionally lose

25% random

10% real prediction

Medium Mode

50% counter predicted move

50% pure random

Hard Mode

Uses Markov prediction (order-2 → order-1 fallback)

Always chooses the perfect counter

▶️ How to Run Locally
1️⃣ Install dependencies
pip install flask

2️⃣ Run the server
python server.py

3️⃣ Open in browser
http://127.0.0.1:5000/

🌐 Deployment (Render / Railway / Heroku)

This project can be deployed on:

Render

Railway

Heroku

You only need these files:

server.py
requirements.txt
Procfile


Example Procfile:

web: gunicorn server:app


Example requirements.txt:

Flask
gunicorn

🥇 What This Project Demonstrates (Perfect for Viva)

✔ Python backend & Flask routing
✔ AI decision-making with pattern recognition
✔ Good UI/UX design
✔ JSON-based data persistence
✔ Defensive programming (timeouts, invalid moves)
✔ Clean project structure
✔ Deployment-ready web app


🙌 Contributors

Arpito Sadhu
Nafis Farhan
