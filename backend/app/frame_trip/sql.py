from app.database.const import FRAME_TRIPS_TABLE


def get_all_trip_ids_sql(group_id, offset, limit):
    return f'''
      SELECT DISTINCT ID
      FROM {FRAME_TRIPS_TABLE}
      WHERE group_id = {group_id}
      ORDER BY ID
      LIMIT {limit}
      OFFSET {offset}
    '''


def get_trip_by_id_sql(trip_id, max_group_id):
    sql = 'SELECT GROUP_ID, IX, IY,'
    for i in range(1, 30):
        sql += f'''
        Ix + P{i}x AS LON,
        Iy + P{i}y AS LAT'''
        sql += ',' if i < 29 else ''
    sql += f'''
    FROM {FRAME_TRIPS_TABLE}
    WHERE ID = {trip_id}
    AND GROUP_ID <= {max_group_id}
    ORDER BY GROUP_ID
    '''
    return sql
