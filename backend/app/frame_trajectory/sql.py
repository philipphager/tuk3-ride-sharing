from app.database.const import FRAME_TABLE


def get_all_trajectory_ids_sql():
    return f'''
      SELECT DISTINCT TID
      FROM {FRAME_TABLE}
    '''


def get_trajectory_by_id_sql(trajectory_id):
    sql = 'SELECT FGID, IX, IY,'
    for i in range(1, 120):
        sql += f'''
        Ix + P{i}x AS LON,
        Iy + P{i}y AS LAT'''
        sql += ',' if i < 119 else ''
    sql += f'''
    FROM {FRAME_TABLE} WHERE TID = {trajectory_id}
    ORDER BY FGID
    '''
    return sql
