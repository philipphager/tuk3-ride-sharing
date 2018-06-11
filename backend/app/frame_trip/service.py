from app.database.hana_connector import HanaConnection
from app.frame_trip.sql import get_all_trip_ids_sql, get_trip_by_id_sql
from app.geojson.frame_converter import frame_to_geojson, \
    trip_ids_to_json, frame_to_point_with_limit
from app.utils import timer


@timer
def get_all_trip_ids(offset, limit):
    with HanaConnection() as connection:
        connection.execute(get_all_trip_ids_sql(offset, limit))
        return trip_ids_to_json(connection.fetchall())


@timer
def get_trip_by_id(trip_id, max_time):
    with HanaConnection() as connection:
        # 900 = 60 Seconds per Minute * 15 Minutes per frames
        max_group = max_time // 900
        max_frame = max_time // 30
        connection.execute(get_trip_by_id_sql(trip_id, max_group))
        data = connection.fetchall()
        return frame_to_geojson(frame_to_point_with_limit(data, max_group, max_frame))
