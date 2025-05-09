import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask.json.provider import DefaultJSONProvider
from bson.objectid import ObjectId

from Persistencia.AgenteBD import MongoDBAgent

from auth import auth_bp
from vehicle import vehicle_bp
from map import map_bp
from reserve import reserve_bp
from chatbot import chatbot_bp
from Dominio.utils import format_number

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# --- Codificador JSON personalizado ---
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
# ------------------------------------

# Calcula la ruta absoluta a /Presentacion/templates
BASE_DIR = os.path.dirname(__file__)         # => Dominio/
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'Presentacion', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'Presentacion', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.json_provider_class = CustomJSONProvider
app.json = app.json_provider_class(app)
app.jinja_env.filters['format_number'] = format_number
app.secret_key = os.getenv("FLASK_SECRET_KEY")


# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(reserve_bp, url_prefix='/reserve')
app.register_blueprint(map_bp, url_prefix='/map')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

@app.route('/')
def home():
    return redirect(url_for('auth.login_page'))

# Conectar a MongoDB
mongo_agent = MongoDBAgent()
if not mongo_agent.client:
    print("Error al conectar con MongoDB")
    exit(1)

if __name__ == '__main__':
    # Escucha en todas las IPs (0.0.0.0) y puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)