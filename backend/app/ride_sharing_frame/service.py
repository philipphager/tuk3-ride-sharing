from app.database.hana_connector import HanaConnection
from app.frame_trip.service import to_geojson
from app.geojson.frame_converter import _timestamp
from app.ride_sharing_frame.sql import get_shared_rides_sql, get_start_and_end


def get_shared_rides(trip_id, threshold):
    with HanaConnection() as connection:
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

        connection.execute(get_shared_rides_sql(start_lon, start_lat, start_group, start_frame, end_lon,
                                                end_lat, end_group, end_frame, threshold))
        cursor = connection.fetchall()
        trip_data = frame_to_point_trips(cursor)
        return [to_geojson(*trip) for trip in trip_data]


def frame_to_point_trips(cursor):
    trips = []
    points = []
    timestamps = []
    trip_id = None

    for frame_group in cursor:
        frame_group = list(frame_group)
        if trip_id != frame_group[0]:
            if trip_id:
                trips.append((trip_id, points, timestamps))
            trip_id = frame_group[0]
            points = []
            timestamps = []
        frame_group.pop(0)  # remove trip_id
        group_id = frame_group[0]
        frames = frame_group[1:]
        i = 0

        while i < len(frames):
            if not frames[i] or frames[i] == 0:
                i += 1
                continue

            time = _timestamp(group_id, i)

            points.append((frames[i], frames[i + 1]))
            timestamps.append(time)
            i += 2

    trips.append((trip_id, points, timestamps))
    return trips
