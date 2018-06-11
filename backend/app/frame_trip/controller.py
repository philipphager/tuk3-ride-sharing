from flask import Blueprint, jsonify

from app.error.DatabaseNotConnected import DatabaseConnectionError
from app.frame_trip.service import get_all_trajectory_ids, get_all_trip_ids, get_trip_by_id

frame_trip_controller = Blueprint('frame-trip', __name__)


@frame_trip_controller.route('/')
def trajectory_ids():
    data = get_all_trajectory_ids()
    return jsonify(data)


@frame_trip_controller.route('/<trajectory_id>/trip')
def trip_ids(trajectory_id):
    data = get_all_trip_ids(trajectory_id)
    return jsonify(data)


@frame_trip_controller.route('/<trajectory_id>/trip/<trip_id>')
def trajectory(trajectory_id, trip_id):
    data = get_trip_by_id(trajectory_id, trip_id)
    return jsonify(data)


@frame_trip_controller.errorhandler(DatabaseConnectionError)
def handle_database_connection_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
