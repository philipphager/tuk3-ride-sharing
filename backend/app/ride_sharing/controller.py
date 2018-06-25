from flask import Blueprint

from app.ride_sharing.service import get_shared_rides

ride_sharing_controller = Blueprint('shared_rides', __name__)


@ride_sharing_controller.route('/<trip_id>/<distance>')
def get_shared_rides_for_trips(trip_id, distance):
    threshold = distance / 60 / 1852  # 1 Grad = 60 min, 1 min = 1852 m
    data = get_shared_rides(trip_id, threshold)
    return data
