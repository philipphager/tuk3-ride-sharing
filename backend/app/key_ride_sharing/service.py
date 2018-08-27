import ast
import json

from app.database.hana_connector import HanaConnection
from app.geojson.geojson_utils import create_geojson
from app.key_ride_sharing.sql import get_ride_by_id_sql, get_shared_ride_candidates_sql
from app.utils import timer


@timer
def get_shared_rides(trip_id, max_distance, max_time):
    with HanaConnection() as connection:
        connection.execute(get_ride_by_id_sql(trip_id))
        trip = convert_trip(connection.fetchone())

        connection.execute(get_shared_ride_candidates_sql(trip, max_distance, max_time))
        cursor = connection.fetchall()
        trips = []
        for row in cursor:
            shared_trip = to_geojson(row, trip, max_distance, max_time)
            if shared_trip:
                trips.append(shared_trip)
    return trips, connection.execution_time


def to_geojson(row, trip, max_distance, max_time):
    timestamps = []
    points = []
    trip_id = row[0]
    nclob = row[1].read()
    samples = json.loads(nclob)
    start_is_in_distance = False
    end_is_in_distance = False
    geojson = None

    for sample in samples:
        timestamp = sample[0]
        timestamps.append(timestamp)
        points.append((sample[1], sample[2]))

        if not euclidean_distance(sample[1], trip['start_point'][0], sample[2], trip['start_point'][1]) <= max_distance \
                and abs(trip['start_time'] - timestamp) <= max_time:
            start_is_in_distance = True

        if euclidean_distance(sample[1], trip['end_point'][0], sample[2], trip['end_point'][1]) <= max_distance \
                and abs(trip['end_time'] - timestamp) <= max_time:
            end_is_in_distance = True

    if start_is_in_distance and end_is_in_distance:
        start = timestamps[0]
        end = timestamps[-1]
        duration = end - start
        geojson = create_geojson(trip_id, points, timestamps, start, end, duration)

    return geojson


def euclidean_distance(x1, x2, y1, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def convert_trip(cursor):
    trip_id = int(cursor[0])
    nclob = cursor[1].read()
    samples = json.loads(nclob)
    start_point = (samples[0][1], samples[0][2])
    end_point = (samples[-1][1], samples[-1][2])
    start_time = cursor[2]
    end_time = cursor[3]
    min_x = cursor[4]
    min_y = cursor[5]
    max_x = cursor[6]
    max_y = cursor[7]
    return {
        'trip_id': trip_id,
        'start_point': start_point,
        'end_point': end_point,
        'start_time': start_time,
        'end_time': end_time,
        'min_x': min_x,
        'min_y': min_y,
        'max_x': max_x,
        'max_y': max_y,
    }
