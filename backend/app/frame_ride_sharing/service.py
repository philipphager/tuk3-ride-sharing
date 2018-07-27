import time

from app.database.hana_connector import HanaConnection
from app.frame_ride_sharing.sql import get_start_and_end, get_frame_shared_rides
from app.frame_trip.service import to_geojson
from app.geojson.frame_converter import frame_to_point_trips
from app.utils import timer


def get_shifted_frames(frame_id, group_id, shift):
    shifted_frames = set()

    # All frames after frame
    for i in range(0, shift + 1):
        shifted_frame_id = frame_id + i
        shifted_group = min(group_id + shifted_frame_id // 30, 96)
        shifted_frame_id = shifted_frame_id % 30
        shifted_frames.add((shifted_group, shifted_frame_id))

    # All frames before frame
    for i in reversed(range(0, shift + 1)):
        shifted_frame_id = frame_id + i
        shifted_group = max(group_id + shifted_frame_id // 30, 1)
        shifted_frame_id = shifted_frame_id % 30
        shifted_frames.add((shifted_group, shifted_frame_id))

    return sorted(shifted_frames)


@timer
def get_shared_rides(trip_id, threshold, max_time):
    with HanaConnection() as connection:
        start_time = time.time()
        # Get data from original trip
        connection.execute(get_start_and_end(trip_id))
        start_group, start_frame, end_group, end_frame = connection.fetchone()

        print('Get data from trip: {} ms'.format((time.time() - start_time) * 1000))

        start_time = time.time()
        shift = max_time // 30
        shifted_start_frames = get_shifted_frames(start_frame, start_group, shift)
        shifted_end_frames = get_shifted_frames(end_frame, end_group, shift)

        connection.execute(get_frame_shared_rides(trip_id, start_group, start_frame, end_group, end_frame,
                                                  shifted_start_frames, shifted_end_frames, threshold))
        cursor = connection.fetchall()
        trip_data = frame_to_point_trips(cursor)
        geojson = [to_geojson(*trip) for trip in trip_data]
        print('Fetch shared rides: {} ms'.format((time.time() - start_time) * 1000))

        return geojson, connection.execution_time
