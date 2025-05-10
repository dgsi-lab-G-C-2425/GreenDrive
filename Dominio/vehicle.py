import sys
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from Persistencia.DAOS.VehiculoDAO import VehiculoDAO
from Persistencia.AgenteBD import MongoDBAgent
from bson.objectid import ObjectId
from Persistencia.DAOS.ReservasDAO import ReservasDAO
from datetime import datetime
from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler


MongoDBAgent = MongoDBAgent()
vehicle_bp = Blueprint('vehiculo', __name__)

@vehicle_bp.route('/')
def index():
    return render_template('vehicleList.html')

@vehicle_bp.route('/vehiculos', methods=['GET'])
def vehicle_list():
    # redirigir si el usuario tiene reserva activa
    user_id = session.get('user_id')
    if user_id and ReservasDAO().get_active_reservation(user_id):
        return redirect(url_for('reserve.index'))

    raw = VehiculoDAO.obtener_todos()
    if raw is None:
        flash("No se encontraron vehículos en la base de datos.", "error")
        return redirect(url_for('vehiculo.index'))
    # convertir _id a str
    vehiculos = [{**v, '_id': str(v.get('_id'))} for v in raw]
    return render_template(
        'vehicleList.html',
        vehiculos=vehiculos,
        google_api_key=os.getenv('GOOGLE_API_KEY'),
        id_usuario=user_id
    )

@vehicle_bp.route('/vehiculos/json', methods=['GET'])
def vehiculos_json():
    raw = VehiculoDAO.obtener_todos()
    vehiculos = [{**v, '_id': str(v.get('_id'))} for v in raw]
    return jsonify(vehiculos), 200

@vehicle_bp.route('/vehiculos/detalles/<id>', methods=['GET'])
def vehiculo_detalles(id):
    try:
        vehiculo = VehiculoDAO.obtener_dato({'_id': ObjectId(id)})
        if vehiculo:
            vehiculo['_id'] = str(vehiculo.get('_id'))
            return jsonify(vehiculo), 200
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    except Exception as e:
        print(f"[ERROR] Detalles vehículo id={id}: {e}")
        return jsonify({'error': str(e)}), 500

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

def actualizar_bateria_periodica():
    import random
    vehiculos = VehiculoDAO.obtener_todos()
    updated_count = 0
    for vehiculo in vehiculos:
        estado = vehiculo.get('estado')
        update_fields = {}
        if estado in ['disponible', 'ocupado']:
            bateria_obj = vehiculo.get('bateria', {})
            nivel = bateria_obj.get('nivel_pct', 0)
            try:
                nivel_val = int(nivel)
            except (ValueError, TypeError):
                nivel_val = 0
            
            if estado == 'disponible':
                incremento = 10  # Aumentar un 10%
                nuevo_nivel = nivel_val + incremento if nivel_val + incremento <= 100 else 100
                update_fields['bateria.nivel_pct'] = nuevo_nivel
            elif estado == 'ocupado':
                decremento = 5   # Disminuir un 5%
                nuevo_nivel = nivel_val - decremento if nivel_val - decremento >= 0 else 0
                update_fields['bateria.nivel_pct'] = nuevo_nivel
                # Establecer velocidad aleatoria entre 0 y 135
                update_fields['ubicacion.velocidad_kmh'] = random.randint(0, 135)
            
            if update_fields:
                resultado = VehiculoDAO.actualizar_dato(
                    {'_id': vehiculo.get('_id')},
                    update_fields
                )
                if getattr(resultado, 'modified_count', 0) > 0:
                    updated_count += 1
    print(f"[INFO] Actualización periódica de batería y velocidad: {updated_count} vehículos actualizados.")
    
@vehicle_bp.route('/vehiculos/<id>/bloquear', methods=['POST'])
def bloquear(id):
    """Bloquea o desbloquea el vehículo."""
    data = request.get_json()
    locked = data.get('locked', True)
    res = VehiculoDAO.actualizar_dato({'_id': ObjectId(id)}, {'bloqueo.locked': locked, 'bloqueo.timestamp': datetime.utcnow()})
    status = 'success' if getattr(res, 'modified_count',0) else 'error'
    return jsonify({'status': status}), 200 if status=='success' else 400

@vehicle_bp.route('/vehiculos/<id>/pinchazo', methods=['POST'])
def reportar_pinchazo(id):
    """Marca pinchazo en una rueda específica."""
    data = request.get_json()
    posicion = data.get('posicion')  # ejemplo: 'FL'
    campo = f"neumaticos.$[elem].estado"
    res = VehiculoDAO.actualizar_dato(
        {'_id': ObjectId(id)},
        {campo: 'pinchazo'},
        array_filters=[{'elem.posicion': posicion}]
    )
    return jsonify({'status': 'success' if res.modified_count else 'error'}), 200

@vehicle_bp.route('/vehiculos/<id>/actualizar_estado', methods=['PUT'])
def actualizar_estado(id):
    """Actualiza el estado general del vehículo."""
    nuevo = request.get_json().get('estado')
    res = VehiculoDAO.actualizar_dato({'_id': ObjectId(id)}, {'estado': nuevo})
    return jsonify({'status': 'success' if res.modified_count else 'error'}), 200


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(actualizar_bateria_periodica, 'interval', minutes=1)
    scheduler.start()
    # opcionalmente guardar el scheduler en current_app para controlarlo después
    current_app.config['BATTERY_SCHEDULER'] = scheduler

@vehicle_bp.before_app_request
def initialize_scheduler():
    start_scheduler()

@vehicle_bp.route('/api/vehicle_status')
def vehicle_status():
    vehiculos = VehiculoDAO.obtener_todos()
    return jsonify([
        {'matricula': v.get('matricula'), 'bateria': v.get('bateria', {}).get('nivel_pct')}
        for v in vehiculos
    ])