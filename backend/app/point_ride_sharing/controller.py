from flask import Blueprint, jsonify, request

from app.point_ride_sharing.service import get_shared_rides

point_ride_sharing_controller = Blueprint('point_shared_rides', __name__)


@point_ride_sharing_controller.route('/<trip_id>')
def get_shared_rides_for_trips(trip_id):
    max_time = request.args.get('max_time', 30, int)
    distance = request.args.get('max_distance', 500, int)
    max_distance = distance / 111120  # 1 Grad = 60 min, 1 min = 1852 m, 60 * 1852
    trips = get_shared_rides(trip_id, max_distance, max_time)
    return jsonify(trips)
