from flask import Flask
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__)
cors = CORS(app, resources={"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('pyhdb').setLevel(logging.WARNING)

DATA_FOLDER = 'data'
PORT = 8000


@app.route('/')
@cross_origin(supports_credentials=True,
              origin='*',
              headers=['Content-Type', 'Authorization'])
def home():
    return "Hello World"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
