import sys
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from Persistencia.DAOS.VehiculoDAO import VehiculoDAO
from Persistencia.AgenteBD import MongoDBAgent
from bson.objectid import ObjectId
from Persistencia.DAOS.ReservasDAO import ReservasDAO
from datetime import datetime

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
    user_id = session.get('user_id')  # obtiene id de usuario en sesión
    return render_template(
        'vehicleList.html',
        vehiculos=vehiculos,
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        id_usuario=user_id
    )

@vehicle_bp.route('/vehiculos/<id>/reservar', methods=['PUT'])
def reservar_vehiculo(id):
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        if not id_usuario:
            return jsonify({'status': 'error', 'message': 'id_usuario no proporcionado'}), 400

        filtro = {'_id': ObjectId(id)}
        resultado = VehiculoDAO.actualizar_dato(filtro, {'estado': 'ocupado'})
        if getattr(resultado, 'matched_count', 0) > 0:
            # crear reserva
            ReservasDAO.insertar_dato({
                'id_usuario': ObjectId(id_usuario),
                'id_vehiculo': ObjectId(id),
                'fecha_inicio': datetime.utcnow(),
                'fecha_fin': None,
                'estado': 'activa'
            })
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
    id_usuario = data.get('id_usuario')
    if not id_usuario:
        return jsonify({'status': 'error', 'message': 'id_usuario no proporcionado'}), 400

    # obtener vehículo y actualizar estado
    vehiculo = VehiculoDAO.obtener_dato({'matricula': matricula})
    if not vehiculo:
        return jsonify({'status': 'error', 'message': 'Vehículo no encontrado'}), 400
    resultado = VehiculoDAO.actualizar_dato({'matricula': matricula}, {'estado': 'ocupado'})
    if getattr(resultado, 'modified_count', 0) > 0:
        # crear reserva
        ReservasDAO.insertar_dato({
            'id_usuario': ObjectId(id_usuario),
            'id_vehiculo': vehiculo.get('_id'),
            'fecha_inicio': datetime.utcnow(),
            'fecha_fin': None,
            'estado': 'activa'
        })
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'No se actualizó ningún registro'}), 400