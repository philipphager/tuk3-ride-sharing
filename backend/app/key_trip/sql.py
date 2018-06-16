from app.database.const import KEY_TRIPS_TABLE


def get_all_trip_ids_sql(offset, limit):
    return f'''
        SELECT DISTINCT ID
        FROM {KEY_TRIPS_TABLE}
        LIMIT {limit}
        OFFSET {offset}
    '''


def get_trip_by_id_sql(trip_id):
    sql = f'''
    SELECT *
    FROM {KEY_TRIPS_TABLE}
    WHERE ID = {trip_id}
    '''
    return sql

