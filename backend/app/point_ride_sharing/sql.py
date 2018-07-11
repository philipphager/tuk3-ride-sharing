def get_shared_rides_sql(trip_id, max_distance, max_time):
    return f'''
        SELECT *
        FROM TUK3_HNKS.Point_Trips
        WHERE id IN (
            SELECT Trip_Start.id
            FROM 
                (SELECT timestamp, lon, lat FROM TUK3_HNKS.Point_Trips WHERE id = {trip_id} ORDER BY timestamp ASC LIMIT 1) S,
                (SELECT timestamp, lon, lat FROM TUK3_HNKS.Point_Trips WHERE id = {trip_id} ORDER BY timestamp DESC LIMIT 1) E,
                TUK3_HNKS.Point_Trips Trip_Start INNER JOIN TUK3_HNKS.Point_Trips Trip_End
                ON Trip_Start.id = Trip_End.id
            WHERE Trip_Start.timestamp BETWEEN (S.timestamp - {max_time}) AND (S.timestamp + {max_time})
            AND Trip_End.timestamp BETWEEN (E.timestamp - {max_time}) AND (E.timestamp + {max_time})
            AND SQRT(POWER(Trip_Start.lon -  S.lon, 2) + POWER(Trip_Start.lat -  S.lat, 2)) <= {max_distance}
            AND SQRT(POWER(Trip_End.lon -  E.lon, 2) + POWER(Trip_End.lat -  E.lat, 2)) <= {max_distance}
        )
        ORDER BY id, timestamp;
    '''
