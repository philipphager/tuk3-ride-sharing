from copy import copy

from app.database.hana_connector import HanaConnection

with HanaConnection() as connection:
    sql = 'SELECT ID, GROUP_ID, '
    for i in range(0, 30):
        sql += f'''
                Ix + P{i}x AS LON,
                Iy + P{i}y AS LAT'''
        sql += ',' if i < 29 else ''
    sql += f'''
    FROM FRAME_TRIPS ORDER BY ID, GROUP_ID
    '''
    connection.execute(sql)
    cursor = connection.fetchall()
    trips = {}
    trip_id = None
    curr_trip = []
    for item in cursor:
        item = list(item)
        if trip_id == item[0]:
            item.pop(0)
            curr_trip.append(item)
        else:
            trip_id = item[0]
            if curr_trip:
                trips[trip_id] = curr_trip
            item.pop(0)
            curr_trip = [item]
    trips[trip_id] = curr_trip

    for trip_id in trips:
        trip = trips[trip_id]

        start_group = copy(trip[0])
        start_group_id = start_group[0]
        start_group.pop(0)
        for idx, item in enumerate(start_group):
            if item is not None:
                start_frame = int(idx / 2)
                break

        end_group = trip[-1]
        end_group_id = end_group[0]
        end_group.pop(0)
        for idx, item in enumerate(reversed(end_group)):
            if item is not None:
                end_frame = int(30 - (idx / 2) - 1)
                break
        sql = f'''INSERT INTO FRAME_TIMES VALUES (
                    {trip_id}, 
                    {start_group_id}, 
                    {start_frame}, 
                    {end_group_id}, 
                    {end_frame})'''

        connection.execute(sql)
        print(trip_id)