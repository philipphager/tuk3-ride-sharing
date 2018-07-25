from flask import Blueprint, jsonify, request

from app.frame_ride_sharing.service import get_shared_rides_sql

ride_sharing_controller_frame = Blueprint('frame-shared-rides', __name__)


@ride_sharing_controller_frame.route('/<trip_id>')
def get_shared_rides_for_trips(trip_id):
    time = request.args.get('time', 30, int)
    distance = request.args.get('distance', 500, int)
    threshold = distance / 111120  # 1 Grad = 60 min, 1 min = 1852 m, 60 * 1852
    trips = get_shared_rides_sql(trip_id, threshold, time)
    return jsonify(trips)
