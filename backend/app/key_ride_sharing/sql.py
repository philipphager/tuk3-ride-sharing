from app.database.const import KEY_TRIPS_TABLE



def get_ride_by_id_sql(trip_id):
    sql = f'''
    SELECT *
    FROM {KEY_TRIPS_TABLE}
    WHERE ID = {trip_id}
    '''
    return sql


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