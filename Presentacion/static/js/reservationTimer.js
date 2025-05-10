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

  const finishBtn = document.getElementById('finishReservation');
  if (finishBtn) {
    finishBtn.addEventListener('click', () => {
      const modal = document.getElementById('finishModal');
      const msg = document.getElementById('finishMessage');
      const cancelBtn = document.getElementById('cancelBtn');
      const confirmBtn = document.getElementById('confirmBtn');
      // mostrar confirmación
      msg.textContent = '¿Estás seguro de finalizar la reserva?';
      cancelBtn.style.display = 'inline-block';
      confirmBtn.textContent = 'Aceptar';
      modal.classList.add('open');

      cancelBtn.onclick = () => 
        modal.classList.remove('open');
      confirmBtn.onclick = () => {
        // al aceptar, ocultar botones
        cancelBtn.style.display = 'none';
        confirmBtn.style.display = 'none';
        const url = finishBtn.dataset.url;
        fetch(url, { method: 'POST' })
          .then(r => r.json())
          .then(data => {
            // muestra resultado en el mismo modal
            msg.textContent = data.success
              ? `Reserva finalizada correctamente\nPrecio total: ${data.total} €`
              : `Error: ${data.error || 'desconocido'}`;
            // volver a mostrar el botón antes de cambiar texto
            confirmBtn.style.display = 'inline-block';
            confirmBtn.textContent = 'Cerrar';
            confirmBtn.classList.remove('confirm-btn');
            confirmBtn.classList.add('close-btn');
            confirmBtn.disabled = false;
            confirmBtn.onclick = () => {
              modal.classList.remove('open');
              window.location.href = '/vehiculos';
            };
          });
      };
    });
  }
})();
