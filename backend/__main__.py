import logging

from flask import Flask, render_template
from flask_cors import CORS

from app.home.controller import home_controller
from app.trajectory.controller import trajectory_controller

app = Flask(__name__, static_folder="../frontend/dist/", template_folder="../frontend/dist/")
cors = CORS(app, resources={"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(trajectory_controller, url_prefix='/trajectory')
app.register_blueprint(home_controller)

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('pyhdb').setLevel(logging.WARNING)

DATA_FOLDER = 'data'
PORT = 8000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
