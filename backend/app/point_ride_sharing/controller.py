from flask import Blueprint, jsonify, request

from app.point_ride_sharing.service import get_shared_rides

point_ride_sharing_controller = Blueprint('point-shared-rides', __name__)


@point_ride_sharing_controller.route('/<trip_id>')
def get_shared_rides_for_trips(trip_id):
    time = request.args.get('time', 30, int)
    distance = request.args.get('distance', 500, int)
    distance = distance / 111120  # 1 Grad = 60 min, 1 min = 1852 m, 60 * 1852
    trips = get_shared_rides(trip_id, distance, time)
    return jsonify(trips)
