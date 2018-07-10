from app.database.hana_connector import HanaConnection
from app.geojson.geojson_utils import create_geojson
from app.key_ride_sharing.sql import get_ride_by_id_sql, get_shared_ride_candidates_sql
import json
import ast


def get_shared_rides(trip_id, threshold):
    with HanaConnection() as connection:
        connection.execute(get_ride_by_id_sql(trip_id))
        trip_id, start_pt, end_pt, start_t, end_t = unpack_root_trip(connection.fetchone())
        connection.execute(get_shared_ride_candidates_sql(start_t, end_t))
        cursor = connection.fetchall()
        output = []
        for trip in cursor:
            print(trip)
            try:
                geojson_obj_trip = to_geojson(trip, threshold, start_pt, end_pt, start_t, end_t)
            except:
                continue
            if geojson_obj_trip is not None:
                output.append(geojson_obj_trip)
    return output
#            if trip[0] == 23139000 or trip[0] == 23587000 or trip[0] == 25223000 or trip[0] == 26820000 \
#                    or trip[0] == 28778000 or trip[0] == 31955000 or trip[0] == 36360000 or trip[0] == 24177000 \
#                    or trip[0] == 23481000:
#                continue
#            print(trip)


def to_geojson(cursor, threshold, start_pt, end_pt, start_t, end_t):
    timestamps = []
    points = []
    trip_id = int(cursor[0])
    nclob = cursor[1].read()
    samples = json.loads(nclob)
    flag_1 = False
    flag_2 = False
    output = None

    for sample in samples:
        time = sample[0]
        timestamps.append(time)
        points.append((sample[1], sample[2]))
        if time == start_t and ((sample[1] - start_pt[0])**2 + (sample[2] == start_pt[1])**2)**0.5 <= threshold:
            flag_1 = True
        if time == end_t and ((sample[1] - end_pt[0])**2 + (sample[2] - end_pt[1])**2)**0.5 <= threshold:
            flag_2 = True

    start = timestamps[0] if len(timestamps) > 0 else 0
    end = timestamps[-1] if len(timestamps) > 0 else 0
    duration = end - start
    if flag_1 and flag_2:
        output = create_geojson(trip_id, points, timestamps, start, end, duration)
    return output


def unpack_root_trip(cursor):
    trip_id = int(cursor[0])
    mbr_obj = cursor[4]
    mbr = ast.literal_eval(mbr_obj)
    start_pt = (mbr[0], mbr[1])
    end_pt = (mbr[2], mbr[3])
    start_t = cursor[2]
    end_t = cursor[3]
    return trip_id, start_pt, end_pt, start_t, end_t
