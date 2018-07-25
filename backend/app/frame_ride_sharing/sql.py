from app.database.const import FRAME_TRIPS_TABLE


def get_shared_rides_ids_sql(trip_id, start_group, start_frame, end_group, end_frame,
                             start_frames, end_frames, threshold):

    # Generate conditions for all start frames
    sql = f'''
        SELECT 
            DISTINCT s.ID
        FROM 
        (SELECT IX + P{start_frame}X as LON, IY + P{start_frame}Y as LAT FROM TUK3_HNKS.FRAME_TRIPS WHERE ID={trip_id} AND GROUP_ID={start_group} LIMIT 1) s_val,
        (SELECT IX + P{end_frame}X as LON, IY + P{end_frame}Y as LAT FROM TUK3_HNKS.FRAME_TRIPS WHERE ID={trip_id}  AND GROUP_ID={end_group} LIMIT 1) e_val,
        TUK3_HNKS.FRAME_TRIPS s INNER JOIN TUK3_HNKS.FRAME_TRIPS e
        ON s.id = e.id
        WHERE (
        '''
    for i, frame in enumerate(start_frames):
        # Only one of the end frames has to match
        if i > 0:
            sql += 'OR '
        sql += f'''
            (s.group_id = {frame[0]} AND SQRT(POWER(s_val.LON - (s.IX + s.P{frame[1]}X), 2) + POWER(s_val.LAT - (s.IY + s.P{frame[1]}Y), 2)) <= {threshold})
        '''
    sql += ') AND ('

    # Generate conditions for all end frames
    for i, frame in enumerate(end_frames):
        # Only one of the end frames has to match
        if i > 0:
            sql += 'OR '
        sql += f'''
            (e.group_id = {frame[0]} AND SQRT(POWER(e_val.LON - (e.IX + e.P{frame[1]}X), 2) + POWER(e_val.LAT - (e.IY + e.P{frame[1]}Y), 2)) <= {threshold})
        '''

    sql += ')'
    return get_all_rides_sql(sql)


def get_all_rides_sql(subquery):
    frame_columns = ""
    for i in range(0, 30):
        frame_columns += f'''
                 Ix + P{i}x AS LON{i},
                 Iy + P{i}y AS LAT{i}'''
        frame_columns += ',' if i < 29 else ''

    sql = f'''
        SELECT
            ID, GROUP_ID, {frame_columns}
        FROM {FRAME_TRIPS_TABLE}
        WHERE ID in (
            {subquery}
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
