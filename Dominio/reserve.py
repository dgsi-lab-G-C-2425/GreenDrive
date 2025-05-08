from flask import Blueprint, render_template, session, redirect, url_for
from Persistencia.DAOS.VehiculoDAO import VehiculoDAO
from Persistencia.DAOS.ReservasDAO import ReservasDAO
import os

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

