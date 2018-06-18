from app.database.hana_connector import HanaConnection
from app.geojson.frame_converter import frame_to_geojson, \
    trajectory_ids_to_json, frame_to_point
from app.frame_trajectory.sql import get_trajectory_by_id_sql,\
    get_all_trajectory_ids_sql
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
        data = connection.fetchall()
        return frame_to_geojson(frame_to_point(data))
