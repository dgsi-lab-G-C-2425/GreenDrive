from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from Persistencia.DAOS.UserDAO import UserDAO
from Persistencia.AgenteBD import MongoDBAgent

mongo_agent = MongoDBAgent()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('loginRegister.html')

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('loginRegister.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Por favor, completa ambos campos.")
        return redirect(url_for('auth.login_page'))

    usuario = UserDAO.obtener_dato({"email": email})
    if usuario:
        if usuario.get("blocked") == True:
            return redirect(url_for('auth.UserBlock'))
        
        if check_password_hash(usuario.get("pass"), password):
            session['user_id'] = str(usuario["_id"])
            session['user_name'] = usuario.get("name")
            session['user_role'] = usuario.get("role", "user") # Default to 'user' if not set

            # Redigirigir según el rol del usuario
            if session['user_role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                flash("Inicio de sesión exitoso!")
                print("Usuario autenticado:", usuario)
                return redirect(url_for('vehiculo.vehicle_list'))
        else:
            flash("Contraseña incorrecta.")
            return redirect(url_for('auth.login_page'))
    else:
        flash("El correo no está registrado.")
        return redirect(url_for('auth.login_page'))

@auth_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        flash("Todos los campos son obligatorios.")
        return redirect(url_for('auth.login_page'))

    if UserDAO.obtener_dato({"email": email}):
        flash("El correo ya está registrado.")
        return redirect(url_for('auth.login_page'))

    hashed_password = generate_password_hash(password)
    nuevo_usuario = {
        "name": name,
        "email": email,
        "pass": hashed_password,
        "blocked": False,
    }
    UserDAO.insertar_dato(nuevo_usuario)

    usuario = UserDAO.obtener_dato({"email": email})
    if usuario:
        session['user_id'] = str(usuario["_id"])
        session['user_name'] = usuario.get("name")
        flash("Registro exitoso!")
        return redirect(url_for('vehiculo.vehicle_list'))  # Or redirect to a dashboard
    else:
        flash("Error en el registro")
        return redirect(url_for('auth.login_page'))

@auth_bp.route('/UserBlock', methods=['GET'])
def UserBlock():
    return render_template('UserBlocked.html')

@auth_bp.route('/users', methods=['GET'])
def users():
    usuarios = UserDAO.obtener_todos()
    return jsonify(usuarios), 200

@auth_bp.route('/logout', methods=['GET'])
def logout():
    # Elimina los datos de la sesión
    session.clear()
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('auth.login_page'))