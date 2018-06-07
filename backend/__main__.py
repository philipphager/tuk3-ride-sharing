import logging

from flask import Flask, render_template
from flask_cors import CORS

from app.frame_trajectory.controller import frame_trajectory_controller
from app.point_trajectory.controller import point_trajectory_controller

app = Flask(__name__, static_folder="../frontend/dist/",
            template_folder="../frontend/dist/")
cors = CORS(app, resources={"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(frame_trajectory_controller,
                       url_prefix='/frame-trajectory')

app.register_blueprint(point_trajectory_controller,
                       url_prefix='/point-trajectory')


@app.route('/', defaults={'path': ''})
def home(path):
    return render_template('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('pyhdb').setLevel(logging.WARNING)

DATA_FOLDER = 'data'
PORT = 8000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
