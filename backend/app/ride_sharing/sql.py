from app.database.const import FRAME_TRIPS_TABLE


def get_shared_rides_sql(start_lon,
                         start_lat,
                         start_group,
                         start_frame,
                         end_lon,
                         end_lat,
                         end_group,
                         end_frame,
                         threshold
                         ):
    frame_columns = ""
    for i in range(0, 30):
        frame_columns += f'''
              Ix + P{i}x AS LON{i},
              Iy + P{i}y AS LAT{i}'''
        frame_columns += ',' if i < 29 else ''

    lon_lat = ""
    for i in range(0, 30):
        lon_lat += f'''
              LON{i},
              LAT{i}'''
        lon_lat += ',' if i < 29 else ''
    sql = f'''
        SELECT 
            trips.TRIP_ID, 
            trips.GROUP_ID,
            {lon_lat}, 
            shared.DISTANCE_START, 
            shared.DISTANCE_END
        FROM (
            SELECT GROUP_ID, ID as TRIP_ID,{frame_columns}
            FROM {FRAME_TRIPS_TABLE}
            ORDER BY GROUP_ID
        ) trips INNER JOIN (
            SELECT 
                TRIP_ID, 
                DISTANCE_START, 
                DISTANCE_END
            FROM (
                SELECT 
                    s.ID as TRIP_ID, 
                    SQRT(POWER({start_lon} - s.IX + s.P{start_frame}X, 2) + POWER({start_lat} - s.IY + s.P{start_frame}Y, 2)) as DISTANCE_START,
                    SQRT(POWER({end_lon} - e.IX + e.P{end_frame}X, 2) + POWER({end_lat} - e.IY + e.P{end_frame}Y, 2)) as DISTANCE_END
                FROM FRAME_TRIPS s INNER JOIN FRAME_TRIPS e
                    ON s.GROUP_ID = {start_group}
                    AND s.P{start_frame}X IS NOT NULL
                    AND s.P{start_frame}Y IS NOT NULL
                    AND e.GROUP_ID = {end_group}
                    AND e.P{end_frame}X IS NOT NULL
                    AND e.P{end_frame}Y IS NOT NULL
                    AND s.ID = e.ID
            )
            WHERE DISTANCE_START <= {threshold}
            AND DISTANCE_END <= {threshold}
        ) shared
        ON trips.TRIP_ID = shared.TRIP_ID
        '''
    return sql


def get_start_and_end(trip_id):
    sql = f'''
    SELECT 
        FLOOR(ST / 900) + 1 as start_group,
        MOD(FLOOR(ST / 30), 30) as start_frame,
        FLOOR(ET / 900) + 1 as end_group,
        MOD(FLOOR(ET / 30), 30) as end_frame,
        OBJ
    FROM TUK3_HNKS.key_value_trips
    WHERE ID = {trip_id}
    '''
    return sql
