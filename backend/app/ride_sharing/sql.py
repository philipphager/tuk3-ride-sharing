def get_shared_rides_sql():
    # TODO replace mocks
    start_frame = 3
    end_frame = 2
    start_y = 22.556116
    start_x = 114.1503
    end_y = 22.556116
    end_x = 114.1503
    start_group_id = 1
    end_group_id = 2
    threshold = 0.03

    sql = f'''
        SELECT 
            key_value.TRIP_ID, 
            key_value.OBJ,
            frame.DISTANCE_START,
            frame.DISTANCE_END
        FROM (
            SELECT 
                ID as TRIP_ID, 
                OBJ
            FROM KEY_VALUE_TRIPS
        ) key_value
        INNER JOIN (
            SELECT
                TRIP_ID,
                DISTANCE_START,
                DISTANCE_END
            FROM (
                SELECT
                    s.ID as TRIP_ID, 
                    SQRT(POWER({start_x} - s.IX + s.P{start_frame}X, 2) + POWER({start_y} - s.IY + s.P{start_frame}Y, 2)) as DISTANCE_START,
                    SQRT(POWER({end_x} - e.IX + e.P{end_frame}X, 2) + POWER({end_y} - e.IY + e.P{end_frame}Y, 2)) as DISTANCE_END
                FROM FRAME_TRIPS s
                INNER JOIN FRAME_TRIPS e
                ON s.GROUP_ID = {start_group_id}
                AND s.P{start_frame}X IS NOT NULL 
                AND s.P{start_frame}Y IS NOT NULL
                AND e.GROUP_ID = {end_group_id}
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
