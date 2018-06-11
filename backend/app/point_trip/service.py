from app.database.hana_connector import HanaConnection
from app.geojson.frame_converter import frame_to_geojson, \
    trip_ids_to_json
from app.point_trip.sql import get_all_trip_ids_sql, get_trip_by_id_sql
from app.utils import timer


@timer
def get_all_trip_ids(limit):
    with HanaConnection() as connection:
        connection.execute(get_all_trip_ids_sql(limit))
        return trip_ids_to_json(connection.fetchall())


@timer
def get_trip_by_id(trip_id, max_time):
    with HanaConnection() as connection:
        connection.execute(get_trip_by_id_sql(trip_id, max_time))
        return frame_to_geojson(connection.fetchall())
