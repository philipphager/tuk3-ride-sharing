from flask import Blueprint, jsonify, request

from app.key_ride_sharing.service import get_shared_rides

key_ride_sharing_controller = Blueprint('key-shared-rides', __name__)


@key_ride_sharing_controller.route('/<trip_id>')
def get_shared_rides_for_trips(trip_id):
    distance = request.args.get('distance', 500, int)
    threshold = distance / 111120  # 1 Grad = 60 min, 1 min = 1852 m, 60 * 1852
    trips = get_shared_rides(trip_id, threshold)
    return jsonify(trips)
