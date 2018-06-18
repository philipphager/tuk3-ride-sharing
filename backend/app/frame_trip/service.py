from app.database.hana_connector import HanaConnection
from app.frame_trip.sql import get_all_trip_ids_sql, get_trip_by_id_sql
from app.geojson.frame_converter import trip_ids_to_json, frame_to_point_with_limit
from app.geojson.geojson_utils import create_geojson
from app.utils import timer


@timer
def get_all_trip_ids(time, offset, limit):
    with HanaConnection() as connection:
        group_id = (time // 900) + 1
        connection.execute(get_all_trip_ids_sql(group_id, offset, limit))
        return trip_ids_to_json(connection.fetchall())


@timer
def get_trip_by_id(trip_id, max_time):
    with HanaConnection() as connection:
        # 900 = 60 Seconds per Minute * 15 Minutes per frames
        max_group = (max_time // 900) + 1
        connection.execute(get_trip_by_id_sql(trip_id, max_group))
        cursor = connection.fetchall()
        points, timestamps = frame_to_point_with_limit(cursor, max_time)
        return to_geojson(trip_id, points, timestamps)


def to_geojson(trip_id, points, timestamps):
    start = timestamps[0] if len(timestamps) > 0 else 0
    end = timestamps[-1] if len(timestamps) > 0 else 0
    duration = end - start
    return create_geojson(points, trip_id, timestamps, start, end, duration)
