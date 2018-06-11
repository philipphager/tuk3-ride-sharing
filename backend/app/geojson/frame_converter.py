from geojson import Feature, LineString


def frame_to_geojson(frames):
    points = [(frame[0], frame[1]) for frame in frames if frame[0] and frame[0]]
    return Feature(geometry=LineString(points))


def trajectory_ids_to_json(cursor):
    return {'trajectory_ids': [row[0] for row in cursor]}


def frame_to_point(data):
    reshaped_data = []
    for frame in data:
        for i in range(1, len(frame), 2):
            reshaped_data.append((frame[i], frame[i+1]))
    return reshaped_data
