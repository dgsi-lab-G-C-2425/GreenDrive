(function(){
  const display = document.getElementById('elapsedTime');
  if (!display) return;
  const raw = display.dataset.start;                   // fecha UTC guardada
  const startMillis = Date.parse(raw);
  const offsetMs = new Date().getTimezoneOffset() * 60000;
  const startUtc = startMillis - offsetMs;             // compensa zona local
  const pad = n => n < 10 ? '0'+n : n;
  function update() {
    const diff = Date.now() - startUtc;
    const sec = Math.floor(diff/1000)%60;
    const min = Math.floor(diff/60000)%60;
    const hr  = Math.floor(diff/3600000);
    display.textContent = pad(hr)+':'+pad(min)+':'+pad(sec);
  }
  update();
  setInterval(update, 1000);
})();
