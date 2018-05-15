from app.database.const import DB_TABLE


def get_all_trajectory_ids_sql():
    return '''
      SELECT DISTINCT TID 
      FROM SHENZHEN_SHARK_DB_120
    '''


def get_trajectory_by_id_sql(trajectory_id):
    union_string = 'UNION ALL'
    filter_string = f'''WHERE TID = {trajectory_id}'''
    sql = f'''
            SELECT TID,
            FGID,
            Ix AS LON,
            Iy AS LAT
            FROM Taxi.{DB_TABLE}
            {filter_string}
            {union_string}
        '''

    for i in range(1, 119):
        sql += f'''
            SELECT TID,
            FGID,
            Ix + P{i}x AS LON,
            Iy + P{i}y AS LAT
            FROM Taxi.{DB_TABLE}
            {filter_string}
        '''
        sql += union_string if i < 118 else ''

    return sql
