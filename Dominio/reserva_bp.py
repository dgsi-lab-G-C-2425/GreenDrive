"""
Blueprint de reservas: rutas HTML + API REST
"""
from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    abort,
)
from bson.objectid import ObjectId
from Persistencia.Service.reserva_service import ReservaService
import auth  # usamos auth.get_current_user(request)

reserva_bp = Blueprint("reservas", __name__)


# ---------- HTML ----------
@reserva_bp.route("/reserva", methods=["GET"])
def reserva_form():
    return render_template("reserva.html")  # Jinja2


# ---------- API ----------
API_PREFIX = "/api/reservas"


def _user_id_from_token():
    """Extrae el user_id usando el helper de auth"""
    if not hasattr(auth, "get_current_user"):
        abort(401, description="Función de autenticación no disponible")
    user_id = auth.get_current_user(request)
    if not user_id:
        abort(401, description="Token no válido")
    return user_id


# CREATE --------------------------------------------------
@reserva_bp.route(API_PREFIX, methods=["POST"])
def api_crear_reserva():
    user_id = _user_id_from_token()
    data = request.get_json(force=True)
    data["usuario_id"] = user_id
    reserva_id = ReservaService.crear(data)
    return jsonify({"_id": reserva_id}), 201


# READ LIST ----------------------------------------------
@reserva_bp.route(API_PREFIX, methods=["GET"])
def api_listar_reservas():
    user_id = request.args.get("user") or _user_id_from_token()
    reservas = ReservaService.listar_por_usuario(user_id)
    return jsonify(reservas), 200


# READ ONE -----------------------------------------------
@reserva_bp.route(f"{API_PREFIX}/<reserva_id>", methods=["GET"])
def api_obtener_reserva(reserva_id):
    reserva = ReservaService.obtener(reserva_id)
    if not reserva:
        abort(404, description="Reserva no encontrada")
    return jsonify(reserva), 200


# UPDATE --------------------------------------------------
@reserva_bp.route(f"{API_PREFIX}/<reserva_id>", methods=["PUT"])
def api_actualizar_reserva(reserva_id):
    data = request.get_json(force=True)
    modificadas = ReservaService.actualizar(reserva_id, data)
    if not modificadas:
        abort(404, description="Reserva no encontrada")
    return jsonify({"modified": modificadas}), 200


# DELETE --------------------------------------------------
@reserva_bp.route(f"{API_PREFIX}/<reserva_id>", methods=["DELETE"])
def api_borrar_reserva(reserva_id):
    eliminadas = ReservaService.borrar(reserva_id)
    if not eliminadas:
        abort(404, description="Reserva no encontrada")
    return jsonify({"deleted": eliminadas}), 200