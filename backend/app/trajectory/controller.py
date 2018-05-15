from flask import Blueprint, jsonify

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
