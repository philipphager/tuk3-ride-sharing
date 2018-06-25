from flask import Blueprint, jsonify

from app.ride_sharing.service import get_shared_rides

ride_sharing_controller = Blueprint('shared_rides', __name__)


@ride_sharing_controller.route('/<trip_id>/<threshold>')
def get_shared_rides_for_trips(trip_id, threshold):
    data = get_shared_rides(trip_id, threshold)
    return jsonify(data)
