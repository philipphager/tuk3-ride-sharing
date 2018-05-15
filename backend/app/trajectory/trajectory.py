from app.database.hana_connector import HanaConnection

ALL_TRAJECTORIES = """
    SELECT DISTINCT tid 
    FROM SHENZHEN_SHARK_DB_120
"""


def get_all_trajectory_ids():
    with HanaConnection() as connection:
        connection.execute(ALL_TRAJECTORIES)
        return _map(connection.fetchall())


def _map(cursor):
    return [row[0] for row in cursor]
