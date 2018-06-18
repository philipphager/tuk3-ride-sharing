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


def frame_to_point_with_limit(cursor, max_time):
    points = []
    timestamps = []

    for frame_group in cursor:
        group_id = frame_group[0]
        frames = frame_group[1:]
        i = 0

        while i < len(frames):
            if not frames[i] or frames[i] == 0:
                i += 1
                continue

            time = _timestamp(group_id, i)

            if time < max_time:
                points.append((frames[i], frames[i + 1]))
                timestamps.append(time)
                i += 2
            else:
                break

    return points, timestamps


def _timestamp(group_id, index_in_array):
    frame = (group_id - 1) * 30 + (index_in_array // 2)
    return frame * 30
