from app.database.hana_connector import HanaConnection
from app.geojson.frame_converter import frame_to_geojson,\
    trajectory_ids_to_json, frame_to_point, unpack_key_value_object
from app.key_trajectory.sql import get_all_trajectory_ids_sql,\
    get_trajectory_by_id_sql
from app.utils import timer


@timer
def get_all_trajectory_ids():
    with HanaConnection() as connection:
        connection.execute(get_all_trajectory_ids_sql())
        return trajectory_ids_to_json(connection.fetchall())


@timer
def get_trajectory_by_id(trajectory_id):
    with HanaConnection() as connection:
        connection.execute(get_trajectory_by_id_sql(trajectory_id))
        data = unpack_key_value_object(connection.fetchone())
        return frame_to_geojson(data)
