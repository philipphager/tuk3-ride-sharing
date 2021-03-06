from flask import Blueprint, jsonify, request

from app.error.DatabaseNotConnected import DatabaseConnectionError
from app.frame_trip.service import get_all_trip_ids, get_trip_by_id

frame_trip_controller = Blueprint('frame-trip', __name__)


@frame_trip_controller.route('/')
def trip_ids():
    time = request.args.get('time', 0, int)
    limit = request.args.get('limit', 1000)
    offset = request.args.get('offset', 0)
    data = get_all_trip_ids(time, offset, limit)
    return jsonify(data)


@frame_trip_controller.route('/<trip_id>')
def trip(trip_id):
    max_time = request.args.get('max_time', 86400, int)
    data = get_trip_by_id(trip_id, max_time)
    return jsonify(data)


@frame_trip_controller.errorhandler(DatabaseConnectionError)
def handle_database_connection_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
