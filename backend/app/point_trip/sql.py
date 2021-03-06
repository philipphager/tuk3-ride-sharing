from app.database.const import POINT_TRIPS_TABLE


def get_all_trip_ids_sql(time, offset, limit):
    return f'''
      SELECT DISTINCT ID
      FROM {POINT_TRIPS_TABLE}
      WHERE timestamp = {time}
      ORDER BY ID
      LIMIT {limit}
      OFFSET {offset}
    '''


def get_trip_by_id_sql(trip_id, max_time):
    sql = f'''
    SELECT TIMESTAMP, LON, LAT
    FROM {POINT_TRIPS_TABLE}
    WHERE ID = {trip_id}
    AND TIMESTAMP <= {max_time}
    ORDER BY TIMESTAMP
    '''
    return sql
