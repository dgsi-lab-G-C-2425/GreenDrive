from flask import Blueprint, render_template, session, redirect, url_for
from Persistencia.DAOS.VehiculoDAO import VehiculoDAO

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/admin/dashboard')
def dashboard():
    # Verifica si el usuario es administrador
    if session.get("user_role") != "admin":
        return redirect(url_for('auth.login'))

    # Obtener el listado de vehículos
    vehiculos = VehiculoDAO.obtener_todos()
    return render_template('admin_dashboard.html', vehiculos=vehiculos)