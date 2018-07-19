import json

from app.database.hana_connector import HanaConnection
from app.geojson.geojson_utils import create_geojson
from app.geojson.key_converter import trip_ids_to_json
from app.key_trip.sql import get_all_trip_ids_sql, get_trip_by_id_sql
from app.utils import timer


@timer
def get_all_trip_ids(time, offset, limit):
    with HanaConnection() as connection:
        connection.execute(get_all_trip_ids_sql(time, offset, limit))
        return trip_ids_to_json(connection.fetchall()), connection.execution_time


@timer
def get_trip_by_id(trip_id, max_time):
    with HanaConnection() as connection:
        connection.execute(get_trip_by_id_sql(trip_id))
        return to_geojson(trip_id, connection.fetchone(), max_time), connection.execution_time


def to_geojson(trip_id, cursor, max_time):
    timestamps = []
    points = []
    nclob = cursor[1].read()
    samples = json.loads(nclob)

    for sample in samples:
        time = sample[0]

        if time <= max_time:
            timestamps.append(time)
            points.append((sample[1], sample[2]))
        else:
            break

    start = timestamps[0] if len(timestamps) > 0 else 0
    end = timestamps[-1] if len(timestamps) > 0 else 0
    duration = end - start

    return create_geojson(trip_id, points, timestamps, start, end, duration)
