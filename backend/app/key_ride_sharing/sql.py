from app.database.const import KEY_TRIPS_TABLE


def get_ride_by_id_sql(trip_id):
    sql = f'''
    SELECT *
    FROM {KEY_TRIPS_TABLE}
    WHERE ID = {trip_id}
    '''
    return sql


# all trips within selected trip time frame +- 15 mins, because if not we have to check too many nclobs
# exponentially much for every 5 mins, remove "900" to scan everything possible... 
def get_shared_ride_candidates_sql(trip, distance):
    return f'''
    SELECT * 
    FROM {KEY_TRIPS_TABLE}
    WHERE 
        ST <= {trip['start_time']} 
        AND ET >= {trip['end_time']}
        AND MIN_X < {trip['max_x'] + distance }
        AND MAX_X > {trip['min_x'] - distance}
        AND MIN_Y < {trip['max_y'] + distance}
        AND MAX_Y > {trip['min_y'] - distance}
    '''
