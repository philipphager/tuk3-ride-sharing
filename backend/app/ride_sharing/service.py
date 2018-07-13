import time

from app.database.hana_connector import HanaConnection
from app.geojson.geojson_utils import create_geojson
from app.ride_sharing.sql import get_shared_rides_sql, get_start_and_end
import json


def get_shared_rides(trip_id, threshold):
    with HanaConnection() as connection:
        start_time = time.time()
        connection.execute(get_start_and_end(trip_id))
        start_group, start_frame, end_group, end_frame, data = connection.fetchone()
        sample = json.load(data)
        start_lon = sample[0][1]
        start_lat = sample[0][2]
        end_lon = sample[-1][1]
        end_lat = sample[-1][2]
        print('Get data from trip: {} ms'.format((time.time() - start_time) * 1000))

        start_time = time.time()
        connection.execute(get_shared_rides_sql(start_lon, start_lat, start_group, start_frame, end_lon,
                                                end_lat, end_group, end_frame, threshold))
        cursor = connection.fetchall()
        geojson = [to_geojson(trip) for trip in cursor]
        print('Get shared rides: {} ms'.format((time.time() - start_time) * 1000))

        return geojson


def to_geojson(cursor):
    timestamps = []
    points = []
    trip_id = int(cursor[0])
    nclob = cursor[1].read()
    samples = json.loads(nclob)

    for sample in samples:
        time = sample[0]
        timestamps.append(time)
        points.append((sample[1], sample[2]))

    start = timestamps[0] if len(timestamps) > 0 else 0
    end = timestamps[-1] if len(timestamps) > 0 else 0
    duration = end - start

    return create_geojson(trip_id, points, timestamps, start, end, duration)
