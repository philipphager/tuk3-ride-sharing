from geojson import Feature, LineString

from app.database.hana_connector import HanaConnection
from app.geojson.frame_converter import trip_ids_to_json
from app.point_trip.sql import get_all_trip_ids_sql, get_trip_by_id_sql
from app.utils import timer


@timer
def get_all_trip_ids(offset, limit):
    with HanaConnection() as connection:
        connection.execute(get_all_trip_ids_sql(offset, limit))
        return trip_ids_to_json(connection.fetchall())


@timer
def get_trip_by_id(trip_id, max_time):
    with HanaConnection() as connection:
        connection.execute(get_trip_by_id_sql(trip_id, max_time))
        return to_geojson(connection.fetchall())


def to_geojson(cursor):
    timestamps = []
    points = []
    start = 0
    end = 0
    duration = 0

    for row in cursor:
        timestamps.append(row[0])
        points.append((row[1], row[2]))

    if len(timestamps) > 0:
        start = timestamps[0]
        end = timestamps[-1]
        duration = end - start

    properties = {'timestamps': timestamps, 'start_time': start, 'end_time': end, 'duration_time': duration}
    return Feature(geometry=LineString(points), properties=properties)
