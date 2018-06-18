import json
from geojson import Feature, LineString


def key_value_to_geojson(values):
    points = [(value[0], value[1]) for value in values if value[0] and value[0]]
    return Feature(geometry=LineString(points))


def key_trip_to_geojson(trip):
    timestamps = []
    points = []
    start = 0
    end = 0
    duration = 0
    nclob = trip[1].read()
    samples = json.loads(nclob)

    for sample in samples:
        timestamps.append(sample[0])
        points.append((sample[1], sample[2]))

    if len(timestamps) > 0:
        if trip[2] == timestamps[0]:
            start = trip[2]
        if trip[3] == timestamps[-1]:
            end = trip[3]
        duration = end - start

    properties = {'timestamps': timestamps, 'start_time': start, 'end_time': end, 'duration_time': duration}
    return Feature(geometry=LineString(points), properties=properties)


def trajectory_ids_to_json(cursor):
    return {'trajectory_ids': [row[0] for row in cursor]}


def trip_ids_to_json(cursor):
    return {'trip_ids': [row[0] for row in cursor]}


def unpack_key_value_object(trajectory):
    nclob = trajectory[1].read()
    samples = json.loads(nclob)
    return [(sample[1], sample[2]) for sample in samples]
