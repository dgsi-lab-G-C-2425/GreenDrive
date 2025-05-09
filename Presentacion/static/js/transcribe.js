let recognitionInstance = null;

function transcribe(event) {
    if (event) event.stopPropagation();

    const widget = document.getElementById('emergencyWidget');
    widget.style.display = 'block';
    
    // Inyecta siempre el contenido (para depuración, luego se podría optimizar)
    widget.innerHTML = `
        <div id="chatContainer" class="chat-container">
            <!-- Aquí se mostrarán los mensajes -->
        </div>
        <div id="statusContainer" style="padding: 10px; text-align: center; border-top: 1px solid #ccc;">
            <span id="statusMsg"></span>
            <br>
            <button id="continueBtn" class="btn btn-primary" style="margin-top: 10px;">Continuar Mensajes</button>
            <button id="hangupBtn" class="btn btn-danger" style="margin-top: 10px;">Colgar</button>
        </div>
    `;
    
    // Actualizar estado: indicar que se está escuchando
    const statusMsg = document.getElementById('statusMsg');
    statusMsg.style.display = 'block';
    statusMsg.textContent = 'Escuchando, por favor hable...';
    
    // Configurar el botón "Continuar Mensajes"
    const continueBtn = document.getElementById('continueBtn');
    continueBtn.onclick = function(e) {
        e.stopPropagation();
        transcribe();
    };

    // Configurar el botón "Colgar"
    const hangupBtn = document.getElementById('hangupBtn');
    hangupBtn.onclick = function(e) {
        e.stopPropagation();
        if (recognitionInstance) {
            recognitionInstance.abort();
            recognitionInstance = null;
        }
        widget.style.display = 'none';
    };

    // Evitar que clics dentro del widget lo cierren
    widget.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognitionInstance = recognition;
    recognition.lang = 'es-ES';
    recognition.start();

    recognition.onresult = function(event) {
        // Ocultar el mensaje de estado inicial
        statusMsg.textContent = '';
        statusMsg.style.display = 'none';

        const texto = event.results[0][0].transcript;

        // Añadir el mensaje del usuario al chat
        const chatContainer = document.getElementById('chatContainer');
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble user';
        bubble.textContent = texto;
        chatContainer.appendChild(bubble);

        // Llamar al endpoint del chatbot
        fetch('/chatbot/transcripcion', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => {
            const sysBubble = document.createElement('div');
            sysBubble.className = 'chat-bubble system';
            sysBubble.textContent = data.mensaje;
            chatContainer.appendChild(sysBubble);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        })
        .catch(error => console.error('Error calling chatbot:', error));

        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    recognition.onerror = function(event) {
        console.error('Error en el reconocimiento:', event.error);
        statusMsg.textContent = '';
    };
}

document.getElementById('emergencyBtn').addEventListener('click', function () {
    if (typeof transcribe === 'function') {
        transcribe();
    } else {
        console.error('transcribe.js is not loaded or transcribe function is not defined.');
    }
});