from geojson import Feature, LineString


def frame_to_geojson(frames):
    points = [(frame[0], frame[1]) for frame in frames if frame[0] and frame[0]]
    return Feature(geometry=LineString(points))


def trajectory_ids_to_json(cursor):
    return {'trajectory_ids': [row[0] for row in cursor]}


def trip_ids_to_json(cursor):
    return {'trip_ids': [row[0] for row in cursor]}


def frame_to_point(data):
    reshaped_data = []
    for frame in data:
        for i in range(1, len(frame), 2):
            reshaped_data.append((frame[i], frame[i + 1]))

    return reshaped_data


def frame_to_point_with_limit(data, max_group, max_frame):
    reshaped_data = []
    first_frame_id = 0
    last_frame_id = 0

    for frame in data:
        group_id = frame[0]
        frame_id = group_id * 30
        first_frame_id = frame_id
        i = 1

        while i in range(1, len(frame), 2) and group_id <= max_group and frame_id <= max_frame:
            reshaped_data.append((frame[i], frame[i + 1]))
            frame_id = group_id * 30 + (i // 2)
            if frame[i]:
                last_frame_id = frame_id
            i += 2

    return first_frame_id, last_frame_id, reshaped_data
