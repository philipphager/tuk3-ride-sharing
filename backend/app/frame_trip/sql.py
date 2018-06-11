from app.database.const import FRAME_TRIPS_TABLE


def get_all_trajectory_ids_sql():
    return f'''
      SELECT DISTINCT TRAJECTORY_ID
      FROM {FRAME_TRIPS_TABLE}
    '''


def get_all_trip_ids_sql(trajectory_id):
    return f'''
      SELECT DISTINCT TRIP_ID
      FROM {FRAME_TRIPS_TABLE}
      WHERE TRAJECTORY_ID = {trajectory_id}
    '''


def get_trip_by_id_sql(trajectory_id, trip_id):
    sql = 'SELECT GROUP_ID, IX, IY,'
    for i in range(1, 30):
        sql += f'''
        Ix + P{i}x AS LON,
        Iy + P{i}y AS LAT'''
        sql += ',' if i < 29 else ''
    sql += f'''
    FROM {FRAME_TRIPS_TABLE} 
    WHERE TRAJECTORY_ID = {trajectory_id}
    AND TRIP_ID = {trip_id}
    ORDER BY GROUP_ID
    '''
    return sql
