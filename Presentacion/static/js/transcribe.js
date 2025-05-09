function transcribe() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'es-ES';
    recognition.start();

    recognition.onresult = function(event) {
        const texto = event.results[0][0].transcript;
        // Mostrar el widget con la transcripción
        document.getElementById('transcriptionText').textContent = texto;
        document.getElementById('emergencyWidget').style.display = 'block';

        // Llamar al endpoint del chatbot
        fetch('/chatbot/transcripcion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => console.log(data.mensaje))
        .catch(error => console.error('Error calling chatbot:', error));
    };

    recognition.onerror = function(event) {
        console.error('Error en el reconocimiento:', event.error);
    };
}

document.getElementById('emergencyBtn').addEventListener('click', transcribe);