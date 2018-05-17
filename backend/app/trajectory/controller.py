from flask import Blueprint, jsonify

from app.error.DatabaseNotConnected import DatabaseConnectionError
from app.trajectory.service import get_all_trajectory_ids, get_trajectory_by_id

trajectory_controller = Blueprint('trajectory', __name__)


@trajectory_controller.route('/')
def trajectory_ids():
    data = get_all_trajectory_ids()
    return jsonify(data)


@trajectory_controller.route('/<trajectory_id>')
def trajectory(trajectory_id):
    data = get_trajectory_by_id(trajectory_id)
    return jsonify(data)


@trajectory_controller.errorhandler(DatabaseConnectionError)
def handle_database_connection_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
