from app.database.hana_connector import HanaConnection
from app.geojson.key_converter import trajectory_ids_to_json
from app.key_trajectory.sql import get_all_trajectory_ids_sql,\
    get_trajectory_by_id_sql
from app.key_trip.service import to_geojson
from app.utils import timer


@timer
def get_all_trajectory_ids():
    with HanaConnection() as connection:
        connection.execute(get_all_trajectory_ids_sql())
        return trajectory_ids_to_json(connection.fetchall()), connection.execution_time


@timer
def get_trajectory_by_id(trajectory_id):
    with HanaConnection() as connection:
        connection.execute(get_trajectory_by_id_sql(trajectory_id))
        data = connection.fetchone()
        return to_geojson(data), connection.execution_time
