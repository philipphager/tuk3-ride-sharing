from app.database.const import POINT_TABLE


def get_all_trajectory_ids_sql():
    return f'''
        SELECT DISTINCT ID
        FROM {POINT_TABLE}
    '''


def get_trajectory_by_id_sql(trajectory_id):
    sql = f'''
    SELECT
        LON,
        LAT
    FROM {POINT_TABLE}
    WHERE ID = {trajectory_id}
    ORDER BY HOUR, MINUTE, SECOND
    '''
    return sql
