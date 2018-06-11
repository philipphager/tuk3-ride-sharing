from flask import Blueprint, jsonify

from app.error.DatabaseNotConnected import DatabaseConnectionError
from app.point_trajectory.service import get_all_trajectory_ids,\
    get_trajectory_by_id

point_trajectory_controller = Blueprint('point-trajectory', __name__)


@point_trajectory_controller.route('/')
def trajectory_ids():
    data = get_all_trajectory_ids()
    return jsonify(data)


@point_trajectory_controller.route('/<trajectory_id>')
def trajectory(trajectory_id):
    data = get_trajectory_by_id(trajectory_id)
    return jsonify(data)


@point_trajectory_controller.errorhandler(DatabaseConnectionError)
def handle_database_connection_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
