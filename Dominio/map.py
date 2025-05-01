from flask import Blueprint, render_template
from Persistencia.DAOS.UserDAO import UserDAO
from Persistencia.AgenteBD import MongoDBAgent

mongo_agent = MongoDBAgent()
map_bp = Blueprint('map', __name__)

@map_bp.route('/')
def index():
    return render_template('map.html')