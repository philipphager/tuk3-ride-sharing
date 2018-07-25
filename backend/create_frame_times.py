from app.database.const import FRAME_TRIPS_TABLE
from app.database.hana_connector import HanaConnection


def get_all_trip_ids_sql(limit):
    sql = 'SELECT ID, GROUP_ID,'
    for i in range(0, 30):
        sql += f'''
            Ix + P{i}x AS LON,
            Iy + P{i}y AS LAT'''
        sql += ',' if i < 29 else ''
    sql += f'''
      FROM {FRAME_TRIPS_TABLE}
      ORDER BY ID, GROUP_ID
    '''
    return sql


def insert_frame_times(trip):
    sql = f'''
      INSERT INTO FRAME_TIMES
      VALUES '''
    sql += '({})'.format(', '.join([str(item) for item in trip]))
    return sql


with HanaConnection() as connection:
    connection.execute(get_all_trip_ids_sql(10))
    cursor = connection.fetchall()

    trips = {}
    current_trip = []
    current_trip_id = None
    for trip in cursor:  # type:tuple
        trip = list(trip)
        if current_trip_id != trip[0]:
            if current_trip:
                trips[current_trip_id] = current_trip
                current_trip = []
            current_trip_id = trip[0]
            trip.pop(0)
            current_trip.append(trip)

        else:
            trip.pop(0)
            current_trip.append(trip)

    trips[current_trip_id] = current_trip

    for trip_id in trips.keys():
        print(trip_id)
        trip = trips[trip_id]
        start = [] + trip[0]
        end = [] + trip[-1]
        start_group = start[0]
        end_group = end[0]
        start.pop(0)
        end.pop(0)
        # Get Start and End Frames
        for i, item in enumerate(start):
            if i % 2 == 0:
                if item:
                    start_frame = int(i / 2)
                    break

        for i, item in enumerate(reversed(end)):
            if i % 2 == 0:
                if item:
                    end_frame = int(29 - (i / 2))
                    break

        print('{}, {}; {}, {}'.format(start_group, start_frame, end_group, end_frame))

        values = [trip_id, start_group, start_frame, end_group, end_frame]
        sql = insert_frame_times(values)
        connection.execute(sql)
        connection.fetchall()