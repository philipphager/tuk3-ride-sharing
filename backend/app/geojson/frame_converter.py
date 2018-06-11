from geojson import Feature, LineString
import json


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


def unpack_key_value_object(trajectory):
    trajectory[1].read()
    samples = json.loads(str(trajectory[1]))
    array = []
    for sample in samples:
        array.append((sample[1], sample[2]))
    return array


# def get_sample(sample):
#     print(sample)
#     lat = sample[1]
#     lon = sample[2]
#     date_time = datetime.strptime(sample[0], '%Y-%m-%d %H:%M:%S')
#     timestamp = date_time.hour * 60 * 60 + date_time.minute * 60 + date_time.second
#     return (lat, lon, timestamp)
