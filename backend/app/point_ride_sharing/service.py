from app.database.hana_connector import HanaConnection
from app.geojson.geojson_utils import create_geojson
from app.utils import timer
from app.point_ride_sharing.sql import get_shared_rides_sql


@timer
def get_shared_rides(trip_id, max_distance, max_time):
    with HanaConnection() as connection:
        connection.execute(get_shared_rides_sql(trip_id, max_distance, max_time))
        cursor = connection.fetchall()
        return all_trips_to_geojson(cursor)

def all_trips_to_geojson(cursor):
    trips = []
    trip_to_data = dict()

    for row in cursor:
        trip_id = row[0]

        if trip_id not in trip_to_data:
            trip_to_data[trip_id] = {
                'points': [],
                'timestamps': []
            }

        timestamp = row[1]
        lon = row[2]
        lat = row[5]
        trip_to_data[trip_id]['points'].append((lon, lat))
        trip_to_data[trip_id]['timestamps'].append(timestamp)

    for trip_id, data in trip_to_data.items():
        points = data['points']
        timestamps = data['timestamps']
        start = timestamps[0]
        end = timestamps[-1]
        duration = end - start
        trips.append(create_geojson(trip_id, points, timestamps, start, end, duration))

    return trips
