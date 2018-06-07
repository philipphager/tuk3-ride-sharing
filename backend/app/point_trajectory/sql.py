from app.database.const import TRAJ_POINT


def get_all_trajectory_ids_sql():
    return f'''
        SELECT DISTINCT ID
        FROM {TRAJ_POINT}
    '''


def get_trajectory_by_id_sql(trajectory_id):
    sql = f'''
    SELECT 
        LON,
        LAT
    FROM {TRAJ_POINT}
    WHERE ID = {trajectory_id}
    ORDER BY HOUR, MINUTE, SECOND
    '''
    return sql
