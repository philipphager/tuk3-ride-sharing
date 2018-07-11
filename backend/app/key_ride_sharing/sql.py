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
def get_shared_ride_candidates_sql(trip_st, trip_end):
    sql = f'''
    SELECT * 
    FROM {KEY_TRIPS_TABLE}
    WHERE ST <= {trip_end} 
    AND ST >= {trip_st} - 900
    AND ET >= {trip_st}
    AND ET <= {trip_end} + 900
    '''
    return sql