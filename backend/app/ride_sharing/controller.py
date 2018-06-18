from flask import Blueprint, jsonify

from app.ride_sharing.service import get_shared_rides

ride_sharing_controller = Blueprint('shared_rides', __name__)


@ride_sharing_controller.route('/<trip_id>')
def get_shared_rides_for_trips(trip_id):
    # TODO get start and end from trip_id
    data = get_shared_rides()
    return jsonify(data)
