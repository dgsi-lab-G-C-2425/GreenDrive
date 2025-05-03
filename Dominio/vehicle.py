import sys
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from Persistencia.DAOS.VehiculoDAO import VehiculoDAO
from Persistencia.AgenteBD import MongoDBAgent
from bson.objectid import ObjectId

MongoDBAgent = MongoDBAgent()
vehicle_bp = Blueprint('vehiculo', __name__)

@vehicle_bp.route('/')
def index():
    return render_template('vehicleList.html')

@vehicle_bp.route('/vehiculos', methods=['GET'])
def vehicle_list():
    raw = VehiculoDAO.obtener_todos()
    if raw is None:
        flash("No se encontraron vehículos en la base de datos.", "error")
        return redirect(url_for('vehiculo.index'))
    # convertir _id a str
    vehiculos = [{**v, '_id': str(v.get('_id'))} for v in raw]
    return render_template('vehicleList.html', vehiculos=vehiculos, google_api_key=os.getenv('GOOGLE_API_KEY'))

@vehicle_bp.route('/vehiculos/<id>/reservar', methods=['PUT'])
def reservar_vehiculo(id):
    try:
        filtro = {'_id': ObjectId(id)}
        resultado = VehiculoDAO.actualizar_dato(filtro, {'estado': 'ocupado'})
        print(f"[CTRL] reservar_vehiculo id={id}, matched={getattr(resultado, 'matched_count', None)}, modified={getattr(resultado, 'modified_count', None)}")
        if getattr(resultado, 'matched_count', 0) > 0:
            return jsonify({'status': 'success'}), 200
        return jsonify({'status': 'error', 'message': 'No se encontró documento o sin cambios'}), 400
    except Exception as e:
        print(f"[ERROR] reservar_vehiculo id={id}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@vehicle_bp.route('/vehiculos/reservar', methods=['POST'])
def reservar_por_matricula():
    data = request.get_json()
    matricula = data.get('matricula')
    if not matricula:
        return jsonify({'status': 'error', 'message': 'Matrícula no proporcionada'}), 400
    resultado = VehiculoDAO.actualizar_dato({'matricula': matricula}, {'estado': 'ocupado'})
    if getattr(resultado, 'modified_count', 0) > 0:
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'No se actualizó ningún registro'}), 400