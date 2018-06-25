from app.database.hana_connector import HanaConnection
from app.ride_sharing.sql import get_shared_rides_sql, get_start_and_end
import json


def get_shared_rides(trip_id, threshold):
    with HanaConnection() as connection:
        connection.execute(get_start_and_end(trip_id))
        start_group, start_frame, end_group, end_frame, data = connection.fetchone()
        sample = json.load(data)
        start_lon = sample[0][1]
        start_lat = sample[0][2]
        end_lon = sample[-1][1]
        end_lat = sample[-1][2]
        connection.execute(get_shared_rides_sql(start_lon,
                                                start_lat,
                                                start_group,
                                                start_frame,
                                                end_lon,
                                                end_lat,
                                                end_group,
                                                end_frame,
                                                threshold
                                                )
                           )
        return connection.fetchall()
