from app.database.hana_connector import HanaConnection
from app.frame_trip.sql import get_all_trip_ids_sql, get_trip_by_id_sql
from app.geojson.frame_converter import frame_to_geojson, \
    frame_to_point, trip_ids_to_json
from app.utils import timer


@timer
def get_all_trip_ids(limit):
    with HanaConnection() as connection:
        connection.execute(get_all_trip_ids_sql(limit))
        return trip_ids_to_json(connection.fetchall())


@timer
def get_trip_by_id(trip_id):
    with HanaConnection() as connection:
        connection.execute(get_trip_by_id_sql(trip_id))
        data = connection.fetchall()
        return frame_to_geojson(frame_to_point(data))
