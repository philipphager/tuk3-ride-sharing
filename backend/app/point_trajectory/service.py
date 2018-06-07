from app.database.hana_connector import HanaConnection
from app.geojson.frame_converter import frame_to_geojson,\
    trajectory_ids_to_json, frame_to_point
from app.point_trajectory.sql import get_all_trajectory_ids_sql,\
    get_trajectory_by_id_sql


def get_all_trajectory_ids():
    with HanaConnection() as connection:
        connection.execute(get_all_trajectory_ids_sql())
        return trajectory_ids_to_json(connection.fetchall())


def get_trajectory_by_id(trajectory_id):
    with HanaConnection() as connection:
        connection.execute(get_trajectory_by_id_sql(trajectory_id))
        return frame_to_geojson(connection.fetchall())
