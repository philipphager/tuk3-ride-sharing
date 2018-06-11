from app.database.const import TRAJ_KEY


def get_all_trajectory_ids_sql():
    return f'''
        SELECT DISTINCT TRAJECTORY_ID
        FROM {TRAJ_KEY}
    '''


def get_trajectory_by_id_sql(trajectory_id):
    sql = f'''
    SELECT *
    FROM {TRAJ_KEY}
    WHERE TRAJECTORY_ID = {trajectory_id}
    '''
    return sql
