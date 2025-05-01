import sys
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
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
    vehiculos = VehiculoDAO.obtener_todos()
    if vehiculos is None:
        flash("No se encontraron vehículos en la base de datos.", "error")
        return redirect(url_for('vehiculo.index'))
    return render_template('vehicleList.html', vehiculos=vehiculos)