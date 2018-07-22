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

    sql = f'''
        SELECT 
            key_value.TRIP_ID,
            key_value.OBJ,
            frame.DISTANCE_START,
            frame.DISTANCE_END
        FROM (
            SELECT
                ID as TRIP_ID,
                OBJ from KEY_VALUE_TRIPS
        ) key_value INNER JOIN (
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
        ) frame
        ON key_value.TRIP_ID = frame.TRIP_ID
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
