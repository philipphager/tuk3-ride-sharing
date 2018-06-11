from app.database.hana_connector import HanaConnection
from app.frame_trajectory.sql import get_all_trajectory_ids_sql
from app.frame_trip.sql import get_all_trip_ids_sql, get_trip_by_id_sql
from app.geojson.frame_converter import frame_to_geojson, \
    trajectory_ids_to_json, frame_to_point
from app.utils import timer


@timer
def get_all_trajectory_ids():
    with HanaConnection() as connection:
        connection.execute(get_all_trajectory_ids_sql())
        return trajectory_ids_to_json(connection.fetchall())


@timer
def get_all_trip_ids(trajectory_id):
    with HanaConnection() as connection:
        connection.execute(get_all_trip_ids_sql(trajectory_id))
        return trajectory_ids_to_json(connection.fetchall())


@timer
def get_trip_by_id(trajectory_id, trip_id):
    with HanaConnection() as connection:
        connection.execute(get_trip_by_id_sql(trajectory_id, trip_id))
        data = connection.fetchall()
        return frame_to_geojson(frame_to_point(data))
