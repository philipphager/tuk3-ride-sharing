from flask import Blueprint, jsonify

from app.trajectory.trajectory import get_all_trajectory_ids

trajectory_controller = Blueprint('trajectory', __name__)


@trajectory_controller.route('/')
def trajectory_ids():
    data = get_all_trajectory_ids()
    return jsonify(data)
