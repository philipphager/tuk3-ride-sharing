import csv
from multiprocessing.pool import Pool
from os import remove
import multiprocessing as mp

from database.hana_connector import HanaConnection
from point_ride_sharing.sql import get_shared_rides_sql, get_trip_ids


class RideSharing:
    def __init__(self, output, distance, time, threads=8):
        self.output = output
        self.distance = distance
        self.time = time
        self.trip_to_shared_rides = dict()
        self.threads = threads
        try:
            remove(self.output)
        except FileNotFoundError:
            pass

    def run(self):
        self.get_all_shared_rides()

    def get_all_shared_rides(self):
        with HanaConnection() as connection:
            connection.execute(get_trip_ids())
            cursor = connection.fetchall()

            chunk_size = 10000
            trip_ids = [trip for [trip] in cursor]
            trip_chunks = [trip_ids[i: i + chunk_size] for i in range(0, len(trip_ids), chunk_size)]

            with Pool(self.threads) as p:
                for chunk in trip_chunks:
                    p.apply_async(self.get_shared_rides, args=(chunk,), callback=self.save_rides)
                p.close()
                p.join()
            self.save_to_file()

    def get_shared_rides(self, trip_ids):
        with HanaConnection() as connection:
            rides = dict()
            for trip_id in trip_ids:
                print('Chunk progress:', len(rides), 'Trip id:', trip_id)
                connection.execute(get_shared_rides_sql(trip_id, self.distance, self.time))
                rides[trip_id] = [trip for [trip] in connection.fetchall()]

            return rides

    def save_rides(self, rides):
        self.trip_to_shared_rides.update(rides)
        print('Accumulate rides:', len(self.trip_to_shared_rides))

    def save_to_file(self):
        with open(self.output, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['trip_id', 'count', 'shared_ride_ids'])
            for trip_id, shared_rides in sorted(self.trip_to_shared_rides.items()):
                count = len(shared_rides)
                rides = ','.join(str(ride) for ride in shared_rides)
                print('Saving to file trip id:', trip_id, 'ride count:', count)
                writer.writerow([trip_id, count, rides])
