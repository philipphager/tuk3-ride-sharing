from app.database.const import TRAJ_SHARK_120


def get_all_trajectory_ids_sql():
    return f'''
      SELECT DISTINCT TID
      FROM {TRAJ_SHARK_120}
    '''


def get_trajectory_by_id_sql(trajectory_id):
    sql = 'SELECT FGID, IX, IY,'
    for i in range(1, 120):
        sql += f'''
        Ix + P{i}x AS LON,
        Iy + P{i}y AS LAT'''
        sql += ',' if i < 119 else ''
    sql += '''
    FROM SHENZHEN_SHARK_DB_120 WHERE TID = 32165
    ORDER BY FGID
    '''
    return sql
