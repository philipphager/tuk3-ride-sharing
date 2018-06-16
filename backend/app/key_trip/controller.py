from flask import Blueprint, jsonify, request

from app.error.DatabaseNotConnected import DatabaseConnectionError
from app.key_trip.service import get_all_trip_ids, get_trip_by_id

key_trip_controller = Blueprint('key-trip', __name__)


@key_trip_controller.route('/')
def trip_ids():
    limit = request.args.get('limit', 1000)
    offset = request.args.get('offset', 0)
    data = get_all_trip_ids(offset, limit)
    return jsonify(data)


@key_trip_controller.route('/<trip_id>')
def trip(trip_id):
    data = get_trip_by_id(trip_id)
    return jsonify(data)


@key_trip_controller.errorhandler(DatabaseConnectionError)
def handle_database_connection_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
