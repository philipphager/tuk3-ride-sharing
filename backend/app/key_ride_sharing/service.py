import json
import ast

from app.utils import timer
from app.database.hana_connector import HanaConnection
from app.geojson.geojson_utils import create_geojson
from app.key_ride_sharing.sql import get_ride_by_id_sql, get_shared_ride_candidates_sql


@timer
def get_shared_rides(trip_id, max_distance, max_time):
    with HanaConnection() as connection:
        connection.execute(get_ride_by_id_sql(trip_id))
        trip = convert_trip(connection.fetchone())

        connection.execute(get_shared_ride_candidates_sql(trip['start_time'], trip['end_time']))
        cursor = connection.fetchall()
        trips = []
        for row in cursor:
            if match_mbr(row, trip):
                shared_trip = to_geojson(row, trip, max_distance, max_time)
                if shared_trip:
                    trips.append(shared_trip)
    return trips


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

        if euclidean_distance(sample[1], trip['start_point'][0], sample[2], trip['start_point'][1]) <= max_distance \
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
    mbr = ast.literal_eval(cursor[4])
    return {
        'trip_id': trip_id,
        'start_point': start_point,
        'end_point': end_point,
        'start_time': start_time,
        'end_time': end_time,
        'mbr': mbr
    }


def match_mbr(cursor, trip):
    cursor_mbr = ast.literal_eval(cursor[4])
    if (cursor_mbr[0] < trip['mbr'][2] and cursor_mbr[2] > trip['mbr'][0]
            and cursor_mbr[1] < trip['mbr'][3] and cursor_mbr[3] > trip['mbr'][1]):
        return True
    else:
        return False
