from flask import Blueprint, jsonify, request

from app.error.DatabaseNotConnected import DatabaseConnectionError
from app.frame_trip.service import get_trip_by_id
from app.point_trip.service import get_all_trip_ids

point_trip_controller = Blueprint('point-trip', __name__)


@point_trip_controller.route('/')
def trip_ids():
    limit = request.args.get('limit', 1000)
    offset = request.args.get('offset', 0)
    data = get_all_trip_ids(offset, limit)
    return jsonify(data)


@point_trip_controller.route('/<trip_id>')
def trip(trip_id):
    max_time = request.args.get('max_time', 86400, int)
    data = get_trip_by_id(trip_id, max_time)
    return jsonify(data)


@point_trip_controller.errorhandler(DatabaseConnectionError)
def handle_database_connection_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
