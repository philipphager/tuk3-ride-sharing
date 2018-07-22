from database.hana_connector import HanaConnection
from service.sql import get_random_trips


class Sampler:
    def __init__(self, limit: int):
        self.limit = limit

    def get(self):
        with HanaConnection() as connection:
            connection.execute(get_random_trips(self.limit))
            cursor = connection.fetchall()
            return [trip_id for [trip_id] in cursor]
