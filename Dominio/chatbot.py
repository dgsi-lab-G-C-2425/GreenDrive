from flask import Blueprint, render_template, jsonify, url_for, request
chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/transcripcion', methods=['POST'])
def transcripcion():
    data = request.get_json()
    texto = data.get('texto', '')
    print(f"Texto recibido: {texto}")

    mensaje = diccionario_accidentes(texto)
    print(f"Mensaje: {mensaje}")
    return jsonify({'mensaje': f'{mensaje}'})


def diccionario_accidentes(texto):
    bomberos = "incendio", "bomberos", "fuego", "llama", "incendio", "apagar", "extinguir", "apagar fuego", "extinguir fuego", "incendiado", "en llamas", "quemado"
    ambulacia = "sangrando", "herido", "mareado", "herida", "accidente", "emergencia", "urgente", "hospital", "atencion medica", "medico"
    averia = "pinchado", "averia", "descompuesto", "fallo", "problema", "dañado", "reparar", "mecanico", "reparacion", "averiado", "descompuesta", "batería", "neumatico", "rueda", "motor", "frenos", "transmision", "cambio", "suspension", "electrico", "electronico"
    robo = "robo", "sustraer", "hurtar", "robar", "sustraccion", "hurto", "delito", "delincuente", "ladrón", "coche robado", "vehiculo robado"
    accidente = "accidente", "choque", "colision", "impacto", "accidentado", "accidentado", "accidentada", "accidentados", "accidentadas", "choque frontal", "choque lateral", "colision frontal", "colision lateral"

    match True:
        case _ if any(palabra in texto for palabra in bomberos):
            return "De acuerdo, llamando a los bomberos."
        case _ if any(palabra in texto for palabra in ambulacia):
            return "De acuerdo, llamando a una ambulancia."
        case _ if any(palabra in texto for palabra in averia):
            return "De acuerdo, enviamos a una grua."
        case _ if any(palabra in texto for palabra in robo):
            return "De acuerdo, llamando a la policía."
        case _ if any(palabra in texto for palabra in accidente):
            return "De acuerdo, llamando a los servicios de emergencia."
        case _:
            return "Lo siento, no puedo ayudar con eso. ¿Podrías darme más detalles?"