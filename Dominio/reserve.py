from flask import Blueprint, render_template, session, redirect, url_for
from Persistencia.DAOS.VehiculoDAO import VehiculoDAO
from Persistencia.DAOS.ReservasDAO import ReservasDAO
import os
from datetime import datetime
from flask import jsonify, request

reserve_bp = Blueprint('reserve', __name__)

@reserve_bp.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login_page'))
    # Obtiene la reserva activa del usuario
    reserva = ReservasDAO().get_active_reservation(user_id)
    vehicle = None
    if reserva:
        # busca los datos del vehículo (dict)
        vehicle = VehiculoDAO.obtener_dato({"_id": reserva['id_vehiculo']})
    return render_template('vehicleListReserved.html',
                           reserva=reserva,
                           vehicle=vehicle)

@reserve_bp.route('/finish', methods=['POST'])
def finish_reservation():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error':'no autenticado'}), 401
    reserva = ReservasDAO().get_active_reservation(user_id)
    if not reserva:
        return jsonify({'error':'sin reserva activa'}), 400
    # actualiza reserva
    now = datetime.utcnow()
    ReservasDAO.actualizar_dato({'_id': reserva['_id']},
                                {'fecha_fin': now, 'estado': 'finalizada'})
    # actualiza vehículo
    VehiculoDAO.actualizar_dato({'_id': reserva['id_vehiculo']},
                                {'estado': 'disponible'})
    # calcula importe
    vehicle = VehiculoDAO.obtener_dato({'_id': reserva['id_vehiculo']})
    precio = vehicle.get('precio', 0)
    elapsed = now - reserva['fecha_inicio']
    horas = elapsed.total_seconds() / 3600
    total = precio * horas
    return jsonify({'success': True, 'total': round(total, 2)})

