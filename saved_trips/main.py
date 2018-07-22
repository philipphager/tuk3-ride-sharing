import pandas as pd
from sortedcontainers import SortedDict

PATH = '/Volumes/Samsung_T5/Documents/Uni/tuk3/shared-rides/mapping.csv'
MAX_GUESTS = 4


def make_data_structures(path):
    map_df = pd.read_csv(PATH, header=None, names=['trip_id', 'length', 'similar_trips'])
    map_df = map_df.sort_values(by='length', ascending=False)
    map_df['similar_trips'] = map_df['similar_trips'].apply(lambda x: str(x).split(','))

    dictionary = map_df[['trip_id', 'similar_trips']].set_index('trip_id').to_dict()['similar_trips']

    inverse_dictionary = {}

    for k, v in dictionary.items():
        for el in v:
            if el in inverse_dictionary:
                inverse_dictionary[el].append(k)
            else:
                inverse_dictionary[el] = [k]

    map_df = map_df.drop(columns=['similar_trips'])
    length_dictionary = map_df.set_index('trip_id').to_dict()['length']

    return dictionary, length_dictionary, inverse_dictionary


# do it in O(n^2)
def main():
    dictionary, length_dictionary, inverse_dictionary = make_data_structures(PATH)
    num_trips = 0

    while len(length_dictionary) > 0:
        trip_id = max(length_dictionary, key=length_dictionary.get)

        num_guests = 0

        for possible_guest_id in dictionary[trip_id]:
            if possible_guest_id in length_dictionary:
                num_guests += 1
                del length_dictionary[possible_guest_id]

                for el in inverse_dictionary[possible_guest_id]:
                    if el in length_dictionary:
                        length_dictionary[el] -= 1

            if num_guests == MAX_GUESTS:
                break

        del length_dictionary[trip_id]
        num_trips += 1
        print(str(len(length_dictionary)))

    print('Number of Trips: ' + num_trips)

if __name__ == '__main__':
    main()
