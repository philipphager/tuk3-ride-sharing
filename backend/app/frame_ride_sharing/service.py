import time

from app.database.hana_connector import HanaConnection
from app.frame_trip.service import to_geojson
from app.geojson.frame_converter import frame_to_point_trips
from app.frame_ride_sharing.sql import get_shared_rides_sql, get_start_and_end


def get_shared_rides(trip_id, threshold):
    with HanaConnection() as connection:
        start_time = time.time()
        # Get data from original trip
        connection.execute(get_start_and_end(trip_id))
        data = connection.fetchall()
        has_data = False
        if not data:
            return
        start_data = data[0]
        end_data = data[-1]

        start_lon = 0
        start_lat = 0
        start_group = 0
        start_frame = 0
        for idx, element in enumerate(start_data):
            if idx == 0:
                start_group = element
                continue
            elif idx % 3 == 0:
                if has_data:
                    start_frame = element
                    break
            elif (idx + 1) % 3 == 0:
                if element:
                    start_lat = element
                    has_data = True
            elif (idx + 2) % 3 == 0:
                if element:
                    start_lon = element
        end_lon = 0
        end_lat = 0
        end_frame = 0
        end_group = end_data[0]
        has_data = False
        for idx, element in enumerate(reversed(end_data)):
            if idx % 3 == 0:
                if has_data:
                    break
                end_frame = element
            elif (idx + 1) % 3 == 0:
                if element:
                    end_lon = element
                    has_data = True
            elif (idx + 2) % 3 == 0:
                if element:
                    end_lat = element
        print('Get data from trip: {} ms'.format((time.time() - start_time) * 1000))

        start_time = time.time()
        # get shared rides and format as geojson
        connection.execute(get_shared_rides_sql(start_lon, start_lat, start_group, start_frame, end_lon,
                                                end_lat, end_group, end_frame, threshold))
        cursor = connection.fetchall()
        trip_data = frame_to_point_trips(cursor)
        geojson = [to_geojson(*trip) for trip in trip_data]
        print('Fetch shared rides: {} ms'.format((time.time() - start_time) * 1000))

        return geojson
