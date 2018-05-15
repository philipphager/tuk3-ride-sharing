from flask import Flask
from flask_cors import CORS, cross_origin
import logging

from app.trajectory.controller import trajectory_controller

app = Flask(__name__)
cors = CORS(app, resources={"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(trajectory_controller, url_prefix='/trajectory')

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('pyhdb').setLevel(logging.WARNING)

DATA_FOLDER = 'data'
PORT = 8000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
