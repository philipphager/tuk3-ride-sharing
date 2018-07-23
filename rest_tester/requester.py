import pandas as pd
import requests
import yaml
from json.decoder import JSONDecodeError


def open_yaml(input):
    config = None
    with open(input, encoding='utf-8') as f:
        config = yaml.load(f)
    return config


def run_all_params(input_request, param_data):
    param_names = list(param_data.keys())
    num_parameter_requests = len(param_data[param_names[0]])
    times = []
    db_times = []

    for i in range(num_parameter_requests):
        request_string = input_request
        for param in param_names:
            request_string = request_string.replace(f'<{param}>', str(param_data[param][i]))

        r = requests.get(request_string)

        try:
            time = r.json()['time']
            db_time = r.json()['db_time']
            times.append(time)
            db_times.append(db_time)
            print('requested:', request_string, 'time:', time, 'db_time:', db_time)
        except JSONDecodeError:
            times.append(-1)
            db_times.append(-1)
            print('requested:', request_string, 'Could not parse JSON:', r.text)

    return pd.Series(times), pd.Series(db_times)


def run_endpoint(endpoint_data, request_name):
    param_crossval = list(endpoint_data['requests']['crossval'].keys())
    num_crossval_requests = len(endpoint_data['requests']['crossval'][param_crossval[0]])

    output_df = pd.DataFrame()

    for i in range(num_crossval_requests):
        request_string = endpoint_data['url']
        distance = str(endpoint_data['requests']['crossval']['distance'][i])
        time = str(endpoint_data['requests']['crossval']['time'][i])
        for param in param_crossval:
            request_string = request_string.replace(f'<{param}>', str(endpoint_data['requests']['crossval'][param][i]))

        times, db_times = run_all_params(request_string, endpoint_data['requests']['parameter'])
        output_df[f'{request_name} api_time (distance-{distance},time-{time})'] = times
        output_df[f'{request_name} db_time (distance-{distance},time-{time})'] = db_times

    return output_df


def run_requests(config, output_path):
    for endpoint in config['endpoints']:
        request_name = endpoint['name']
        run_endpoint(endpoint, request_name).to_csv(output_path + '/' + request_name + '.csv', index=False)
