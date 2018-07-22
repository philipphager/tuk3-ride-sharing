import time

from app.database.hana_connector import HanaConnection
from app.frame_trip.service import to_geojson
from app.geojson.frame_converter import frame_to_point_trips
from app.frame_ride_sharing.sql import get_shared_rides_ids_sql, get_start_and_end, get_full_shared_rides_sql


def get_shared_rides(trip_id, threshold, max_time):
    with HanaConnection() as connection:
        start_time = time.time()
        # Get data from original trip
        connection.execute(get_start_and_end(trip_id))
        data = connection.fetchall()
        if not data:
            return

        start_group, start_frame, end_group, end_frame = extract_start_and_end_values(data)

        print('Get data from trip: {} ms'.format((time.time() - start_time) * 1000))

        start_time = time.time()
        shifted_frames = max_time // 30
        trips = set()
        # get shared rides and format as geojson
        connection.execute(
            get_shared_rides_ids_sql(trip_id, start_group, start_frame, end_group, end_frame, threshold))
        cursor = connection.fetchall()
        trips.update(tuple(cursor))

        # shift frames to get trips based on time
        for i in range(1, shifted_frames + 1):
            connection.execute(get_shared_rides_ids_sql(trip_id, start_group, start_frame,
                                                        end_group, end_frame, threshold, + i))
            cursor = connection.fetchall()
            trips.update(tuple(cursor))

            connection.execute(get_shared_rides_ids_sql(trip_id, start_group, start_frame,
                                                        end_group, end_frame, threshold, -i))
            cursor = connection.fetchall()
            trips.update(tuple(cursor))

        cleaned_trips = [trip[0] for trip in trips if trip]
        connection.execute(get_full_shared_rides_sql(cleaned_trips))
        cursor = connection.fetchall()
        trip_data = frame_to_point_trips(cursor)
        geojson = [to_geojson(*trip) for trip in trip_data]
        print('Fetch shared rides: {} ms'.format((time.time() - start_time) * 1000))

        return geojson


def extract_start_and_end_values(data: list):
    """ data example:
    [
        (group0, lon0, frame0, ...)
        (group1, lon0, frame0, ...)
    ]
    """
    start_data = list(data[0])
    end_data = list(data[-1])

    # Extract start values
    start_frame = 0
    start_group = start_data[0]
    start_data.pop(0)
    has_data = False
    for idx, element in enumerate(start_data):
        if (idx + 1) % 2 == 0:
            if has_data:
                start_frame = element
                break
        elif idx % 2 == 0:
            if element:
                has_data = True

    # Extract end values
    end_frame = 0
    end_group = end_data[0]
    has_data = False
    for idx, element in enumerate(reversed(end_data)):
        if idx % 2 == 0:
            if has_data:
                break
            end_frame = element
        elif (idx + 1) % 2 == 0:
            if element:
                has_data = True

    return start_group, start_frame, end_group, end_frame
