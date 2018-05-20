from geojson import Feature, LineString


def frame_to_geojson(frames):
    points = [(frame[3], frame[4]) for frame in frames]
    return Feature(geometry=LineString(points))


def trajectory_ids_to_list(cursor):
    return {'trajectory_ids': [row[0] for row in cursor]}
