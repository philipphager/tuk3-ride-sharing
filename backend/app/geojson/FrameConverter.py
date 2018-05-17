from datetime import datetime

from geojson import Feature, LineString


def frame_to_geojson(frames):
    points = []
    timestamps = []

    for frame in frames:
        points.append((frame[3], frame[4]))
        timestamps.append(frame_id_to_timestamp(frame[1], frame[2]))

    line = LineString(points)
    properties = {'timestamps': timestamps}
    return Feature(geometry=line, properties=properties)


def frame_id_to_timestamp(frame_group_id, frame_id):
    hour = frame_group_id - 1
    minute = frame_id // 2
    second = 0 if frame_id % 2 == 0 else 30
    return datetime(2013, 10, 22, hour, minute, second)


def trajectory_ids_to_list(cursor):
    return {'trajectory_ids': [row[0] for row in cursor]}
