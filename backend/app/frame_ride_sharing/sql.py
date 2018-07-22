from app.database.const import FRAME_TRIPS_TABLE


def get_shared_rides_ids_sql(trip_id, start_group, start_frame, end_group, end_frame, threshold, frame_shift=0):
    shift_start_frame = start_frame + frame_shift
    shift_end_frame = end_frame + frame_shift
    shift_start_group = start_group
    shift_end_group = end_group
    if start_frame + frame_shift < 0:
        shift_start_frame = 30 + frame_shift
        shift_start_group = start_group - 1
    if end_frame + frame_shift < 0:
        shift_end_frame = 30 + frame_shift
        shift_end_group = end_group - 1
    if start_frame + frame_shift > 29:
        shift_start_frame = frame_shift + 1
        shift_start_group = start_group + 1
    if end_frame + frame_shift > 29:
        shift_end_frame = frame_shift + 1
        shift_end_group = end_group + 1

    assert 0 <= shift_start_frame <= 29
    assert 0 <= shift_end_frame <= 29
    assert 1 <= shift_start_group
    assert 1 <= shift_end_group

    sql = f'''
        SELECT 
            s.ID
        FROM 
        (SELECT IX + P{start_frame}X as LON, IY + P{start_frame}Y as LAT FROM FRAME_TRIPS WHERE ID={trip_id} AND GROUP_ID={start_group} LIMIT 1) s_val,
        (SELECT IX + P{end_frame}X as LON, IY + P{end_frame}Y as LAT FROM FRAME_TRIPS WHERE ID={trip_id}  AND GROUP_ID={end_group} LIMIT 1) e_val,
        FRAME_TRIPS s INNER JOIN FRAME_TRIPS e
            ON s.GROUP_ID = {shift_start_group}
            AND s.P{shift_start_frame}X IS NOT NULL
            AND s.P{shift_start_frame}Y IS NOT NULL
            AND e.GROUP_ID = {shift_end_group}
            AND e.P{shift_end_frame}X IS NOT NULL
            AND e.P{shift_end_frame}Y IS NOT NULL
            AND s.ID = e.ID
        WHERE SQRT(POWER(s_val.LON - s.IX + s.P{shift_start_frame}X, 2) + POWER(s_val.LAT - s.IY + s.P{shift_start_frame}Y, 2)) <= {threshold}
        AND SQRT(POWER(e_val.LON - e.IX + e.P{shift_end_frame}X, 2) + POWER(e_val.LAT - e.IY + e.P{shift_end_frame}Y, 2)) <= {threshold}
        '''
    return sql


def get_full_shared_rides_sql(trip_ids):
    frame_columns = ""
    for i in range(0, 30):
        frame_columns += f'''
                 Ix + P{i}x AS LON{i},
                 Iy + P{i}y AS LAT{i}'''
        frame_columns += ',' if i < 29 else ''

    if len(trip_ids) > 0:
        str_trips = ','.join((str(trip) for trip in trip_ids))
    else:
        str_trips = 'NULL'

    sql = f'''
        SELECT
            ID, GROUP_ID, {frame_columns}
        FROM {FRAME_TRIPS_TABLE}
        WHERE ID in ({str_trips})
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
