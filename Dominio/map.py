from flask import Blueprint, render_template, jsonify, url_for
from Persistencia.DAOS.VehiculoDAO import VehiculoDAO
import os

map_bp = Blueprint('map', __name__)

@map_bp.route('/')
def index():
    google_api_key = os.getenv('GOOGLE_API_KEY')
    return render_template('map.html', google_api_key=google_api_key)

@map_bp.route('/data', methods=['GET'])
def map_data():
    vehiculos = VehiculoDAO.obtener_todos() or []
    data = []
    for v in vehiculos:
        ubic = v.get('ubicacion', {})
        lat, lng = ubic.get('lat'), ubic.get('lng')
        if lat is None or lng is None:
            continue
        tipo = v.get('tipo', 'default')
        modelo = v.get('modelo', 'Desconocido')
        # construye la URL al fichero estático
        icon_url = url_for('static', filename=f'images/vehicles/{tipo}.png')
        data.append({
            'lat': lat,
            'lng': lng,
            'icon': icon_url,
            'title': modelo
        })
    return jsonify(data)