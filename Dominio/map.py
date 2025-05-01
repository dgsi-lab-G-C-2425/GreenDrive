from flask import Blueprint, render_template
from Persistencia.DAOS.UserDAO import UserDAO
from Persistencia.AgenteBD import MongoDBAgent
import os

mongo_agent = MongoDBAgent()
map_bp = Blueprint('map', __name__)

@map_bp.route('/')
def index():
    google_api_key = os.getenv("GOOGLE_API_KEY")  # Leer la API key desde .env
    return render_template('map.html', google_api_key=google_api_key)