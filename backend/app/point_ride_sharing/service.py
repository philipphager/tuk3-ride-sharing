from app.database.hana_connector import HanaConnection
from app.geojson.geojson_utils import create_geojson
from app.point_ride_sharing.sql import get_shared_rides_sql
from app.utils import timer


@timer
def get_shared_rides(trip_id, threshold):
    with HanaConnection() as connection:
        connection.execute(get_shared_rides_sql(trip_id, threshold))
        cursor = connection.fetchall()
        return all_trips_to_geojson(cursor)


def all_trips_to_geojson(cursor):
    current_trip_id = -1
    trip_id = -1
    trips = []
    timestamps = []
    points = []

    for row in cursor:
        trip_id = row[0]

        if trip_id != current_trip_id and len(points) > 0:
            current_trip_id = trip_id
            start = timestamps[0]
            end = timestamps[-1]
            duration = end - start
            geojson = create_geojson(trip_id, points, timestamps, start, end, duration)
            trips.append(geojson)
            timestamps = []
            points = []

        timestamp = row[1]
        lon = row[2]
        lat = row[5]
        timestamps.append(timestamp)
        points.append((lon, lat))

    if len(points) > 0:
        start = timestamps[0]
        end = timestamps[-1]
        duration = end - start
        geojson = create_geojson(trip_id, points, timestamps, start, end, duration)
        trips.append(geojson)

    return trips
