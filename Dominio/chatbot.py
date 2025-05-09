from flask import Blueprint, render_template, jsonify, url_for, request
chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/transcripcion', methods=['POST'])
def transcripcion():
    data = request.get_json()
    texto = data.get('texto', '')
    print(f"Texto recibido: {texto}")
    return jsonify({'mensaje': f'Transcripción recibida: {texto}'})
