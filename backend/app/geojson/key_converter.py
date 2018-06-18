import json
from geojson import Feature, LineString


def key_value_to_geojson(values):
    points = [(value[0], value[1]) for value in values if value[0] and value[0]]
    return Feature(geometry=LineString(points))

def trajectory_ids_to_json(cursor):
    return {'trajectory_ids': [row[0] for row in cursor]}


def trip_ids_to_json(cursor):
    return {'trip_ids': [row[0] for row in cursor]}


def unpack_key_value_object(trajectory):
    nclob = trajectory[1].read()
    samples = json.loads(nclob)
    return [(sample[1], sample[2]) for sample in samples]
