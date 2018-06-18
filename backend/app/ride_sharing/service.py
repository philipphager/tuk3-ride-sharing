from app.database.hana_connector import HanaConnection
from app.ride_sharing.sql import get_shared_rides_sql


def get_shared_rides():
    with HanaConnection() as connection:
        connection.execute(get_shared_rides_sql())
        return connection.fetchall()
