import csv
from os import remove

from database.hana_connector import HanaConnection
from point_ride_sharing.sql import get_shared_rides_sql, get_trip_ids


class RideSharing:
    def __init__(self, output, distance, time):
        self.output = output
        self.distance = distance
        self.time = time
        self.trip_to_shared_rides = dict()
        try:
            remove(self.output)
        except FileNotFoundError:
            pass

    def run(self):
        self.get_all_shared_rides()
        self.save_to_file()

    def get_all_shared_rides(self):
        with HanaConnection() as connection:
            connection.execute(get_trip_ids())
            cursor = connection.fetchall()

            for [trip_id] in cursor:
                trips = self.get_shared_rides(trip_id)
                self.trip_to_shared_rides[trip_id] = trips
                print('Trip id:', trip_id, 'Ride sharing candidates:', trips)

    def get_shared_rides(self, trip_id):
        with HanaConnection() as connection:
            connection.execute(get_shared_rides_sql(trip_id, self.distance, self.time))
            return [trip for [trip] in connection.fetchall()]

    def save_to_file(self):
        with open(self.output, mode='a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['trip_id', 'count', 'shared_ride_ids'])
            for trip_id, shared_rides in self.trip_to_shared_rides.items():
                count = len(shared_rides)
                rides = ','.join(str(ride) for ride in shared_rides)
                print('Saving to file trip id:', trip_id, 'ride count:', count)
                writer.writerow([trip_id, count, rides])
