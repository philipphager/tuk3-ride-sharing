from geojson import LineString, Feature


def create_geojson(data, trip_id, timestamps, start, end, duration):
    properties = {
        'trip_id': trip_id,
        'timestamps': timestamps,
        'start_time': start,
        'end_time': end,
        'duration_time': duration
    }
    return Feature(geometry=LineString(data), properties=properties)
