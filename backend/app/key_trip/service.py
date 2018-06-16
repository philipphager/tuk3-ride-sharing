from app.database.hana_connector import HanaConnection
from app.geojson.key_converter import key_trip_to_geojson, \
    trip_ids_to_json, unpack_key_value_object
from app.key_trip.sql import get_all_trip_ids_sql, \
    get_trip_by_id_sql
from app.utils import timer


@timer
def get_all_trip_ids(offset, limit):
    with HanaConnection() as connection:
        connection.execute(get_all_trip_ids_sql(offset, limit))
        return trip_ids_to_json(connection.fetchall())


@timer
def get_trip_by_id(trajectory_id):
    with HanaConnection() as connection:
        connection.execute(get_trip_by_id_sql(trajectory_id))
        return key_trip_to_geojson(connection.fetchone())
