from app.database.const import FRAME_TRIPS_TABLE


def get_all_trajectory_ids_sql():
    return f'''
      SELECT DISTINCT TRAJECTORY_ID
      FROM {FRAME_TRIPS_TABLE}
    '''


def get_all_trip_ids_sql(offset, limit):
    return f'''
      SELECT DISTINCT CONCAT(TRAJECTORY_ID, TRIP_ID)
      FROM {FRAME_TRIPS_TABLE}
      LIMIT {limit}
      OFFSET {offset}
    '''


def get_trip_by_id_sql(trip_id, max_group_id):
    # TODO: Remove!
    trajectory_id = trip_id[:5]
    trip_id = trip_id[5:]

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
    AND GROUP_ID <= {max_group_id}
    ORDER BY GROUP_ID
    '''
    return sql
