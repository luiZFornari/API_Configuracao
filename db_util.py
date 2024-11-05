# db_util.py
import json
from flask_sqlalchemy import SQLAlchemy
import os

# Load componentes from JSON file
def load_componentes():
    with open('componentes2.json', 'r') as json_file:
        return json.load(json_file)

# Configure database URI
def configure_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
