def get_random_trips(limit):
    return f'''
        SELECT ID
        FROM TUK3_HNKS.POINT_TRIPS
        -- Exclude daily trips --
        WHERE ID NOT IN (
            SELECT max_id
            FROM (
                SELECT MAX(ID) as max_id
                FROM TUK3_HNKS.KEY_VALUE_TRIPS
                GROUP BY LEFT(ID, 5)
                ORDER BY LEFT(ID, 5)
            )
            WHERE RIGHT(max_id, 3) = 0
        )
        ORDER BY RAND()
        LIMIT {limit};
    '''
