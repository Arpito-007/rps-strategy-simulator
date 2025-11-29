// script.js: connect frontend to Flask backend
let userScore = 0, aiScore = 0, draws = 0;

async function play(move){
  // visual feedback instantly
  document.getElementById('result-text').innerText = "Playing...";
  document.getElementById('predicted-text').innerText = "";

  try {
    const res = await fetch('/play', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ user_move: move })
    });
    const data = await res.json();
    if(data.error){
      document.getElementById('result-text').innerText = data.error;
      return;
    }

    // update choices
    const aiMove = data.ai_move;
    const predicted = data.predicted;
    const result = data.result;

    // animate chosen button (brief)
    animateChosen(move);

    // update result text and predicted text
    if(result === 'user'){
      userScore += 1;
      document.getElementById('result-text').innerText = "You win this round!";
    } else if(result === 'ai'){
      aiScore += 1;
      document.getElementById('result-text').innerText = "AI wins this round.";
    } else {
      draws += 1;
      document.getElementById('result-text').innerText = "It's a draw.";
    }
    document.getElementById('predicted-text').innerText = `AI predicted: ${predicted}`;

    // update scoreboard
    document.getElementById('user-score').innerText = userScore;
    document.getElementById('ai-score').innerText = aiScore;
    document.getElementById('draws').innerText = draws;

    // highlight AI's choice briefly
    pulseAiChoice(aiMove);

  } catch(err){
    console.error(err);
    document.getElementById('result-text').innerText = "Server error — make sure Flask is running.";
  }
}

function animateChosen(move){
  const id = moveToId(move);
  const el = document.getElementById(id);
  if(!el) return;
  el.classList.add('active');
  setTimeout(()=> el.classList.remove('active'), 300);
}

function moveToId(m){
  if(m==='rock') return 'btn-rock';
  if(m==='paper') return 'btn-paper';
  return 'btn-scissors';
}

function pulseAiChoice(aiMove){
  const id = moveToId(aiMove);
  const el = document.getElementById(id);
  if(!el) return;
  el.style.boxShadow = '0 4px 30px rgba(107,72,39,0.22)';
  setTimeout(()=> el.style.boxShadow = '', 500);
}

// difficulty buttons
document.getElementById('d-easy').addEventListener('click', ()=> setDifficulty('easy'));
document.getElementById('d-medium').addEventListener('click', ()=> setDifficulty('medium'));
document.getElementById('d-hard').addEventListener('click', ()=> setDifficulty('hard'));

async function setDifficulty(level){
  try {
    const res = await fetch('/set_difficulty', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ level })
    });
    const data = await res.json();
    if(data.status === 'ok'){
      // toggle active visuals
      document.querySelectorAll('.diff').forEach(e=> e.classList.remove('active'));

      if(level==='easy') document.getElementById('d-easy').classList.add('active');
      if(level==='medium') document.getElementById('d-medium').classList.add('active');
      if(level==='hard') document.getElementById('d-hard').classList.add('active');

      document.getElementById('result-text').innerText = `Difficulty: ${level.toUpperCase()}`;
      document.getElementById('predicted-text').innerText = '';
    }
  } catch(err){
    console.error(err);
  }
}

// connect button clicks
document.querySelectorAll('.rps-btn').forEach(btn=>{
  btn.addEventListener('click', ()=> {
    const m = btn.getAttribute('data-move');
    play(m);
  });
});