from app.database.const import FRAME_TRIPS_TABLE


def get_shared_rides_sql(trip_id, start_group, start_frame, end_group, end_frame, threshold ):
    frame_columns = ""
    for i in range(0, 30):
        frame_columns += f'''
              Ix + P{i}x AS LON{i},
              Iy + P{i}y AS LAT{i}'''
        frame_columns += ',' if i < 29 else ''

    sql = f'''
            SELECT ID, GROUP_ID, {frame_columns}
            FROM {FRAME_TRIPS_TABLE}
            WHERE ID in (
                SELECT 
                    s.ID
                FROM 
                (SELECT IX + P{start_frame}X as LON, IY + P{start_frame}Y as LAT FROM FRAME_TRIPS WHERE ID={trip_id} AND GROUP_ID={start_group} LIMIT 1) s_val,
                (SELECT IX + P{end_frame}X as LON, IY + P{end_frame}Y as LAT FROM FRAME_TRIPS WHERE ID={trip_id}  AND GROUP_ID={end_group} LIMIT 1) e_val,
                FRAME_TRIPS s INNER JOIN FRAME_TRIPS e
                    ON s.GROUP_ID = {start_group}
                    AND s.P{start_frame}X IS NOT NULL
                    AND s.P{start_frame}Y IS NOT NULL
                    AND e.GROUP_ID = {end_group}
                    AND e.P{end_frame}X IS NOT NULL
                    AND e.P{end_frame}Y IS NOT NULL
                    AND s.ID = e.ID
                WHERE SQRT(POWER(s_val.LON - s.IX + s.P{start_frame}X, 2) + POWER(s_val.LAT - s.IY + s.P{start_frame}Y, 2)) <= {threshold}
                AND SQRT(POWER(e_val.LON - e.IX + e.P{end_frame}X, 2) + POWER(e_val.LAT - e.IY + e.P{end_frame}Y, 2)) <= {threshold}
            )
            ORDER BY ID, GROUP_ID

        '''
    return sql


def get_start_and_end(trip_id):
    sql = 'SELECT GROUP_ID,'
    for i in range(0, 30):
        sql += f'''
           Ix + P{i}x AS LON,
           {i} as FRAME
           '''
        sql += ',' if i < 29 else ''
    sql += f'''
       FROM {FRAME_TRIPS_TABLE}
       WHERE ID = {trip_id}
       ORDER BY GROUP_ID
       '''
    return sql
