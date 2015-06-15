from credentials import uber_credentials
import requests
import copy

def uber_api(latitude, longitude):

    url = 'https://api.uber.com/v1/estimates/time'

    parameters = {
        'server_token': uber_credentials['server_token'],
        'start_latitude': latitude,
        'start_longitude': longitude,
    }

    response_from_uber = requests.get(url, params=parameters)
    dataTime = response_from_uber.json()
    print dataTime

    parameters = {
        'server_token': uber_credentials['server_token'],
        'latitude': latitude,
        'longitude': longitude,
    }

    url = 'https://api.uber.com/v1/products'
    response_from_uber = requests.get(url, params=parameters)
    data = response_from_uber.json()

    ''' ========================Example JSON to be sent===============
    result = {
        'result': [
            {
                'provider': 'provider_name',
                'time_of_arrival': 'time in minutes',
                'price_per_km': 'price in INR/Km',
                'display_name': 'Black/X/GO',
                'min_price': 'minimum_price',
            }
        ],
    }
    =============================================================='''

    result = {
        'result': []
    }

    cab_provider = 'Uber'
    filler_dictionary = {}

    for x_data in dataTime['times']:

        filler_dictionary['provider'] = cab_provider
        filler_dictionary['time_of_arrival'] = int(int(x_data['estimate'])/60)
        filler_dictionary['display_name'] = x_data['display_name']

        for y_data in data['products']:
            if y_data['display_name'] == x_data['display_name']:
                filler_dictionary['price_per_km'] = y_data['price_details']['cost_per_distance']
                filler_dictionary['min_price'] = y_data['price_details']['minimum']

        result['result'].append(copy.deepcopy(filler_dictionary))

    return result['result']


def taxi_for_sure_api(latitude, longitude):

    url = 'http://iospush.taxiforsure.com/getNearestDriversForApp/?density=320&appVersion=4.1.1&longitude='\
          + str(longitude) +'&latitude=' + str(latitude)

    final_list = []
    filler_dict = {}

    data = requests.get(url)
    output = data.json()['response_data']['data']

    for res in output:
        filler_dict['provider'] = 'TaxiForSure'
        filler_dict['time_of_arrival'] = int(res['duration'])
        filler_dict['price_per_km'] = '16'
        filler_dict['display_name'] = res['carType']
        filler_dict['min_price'] = '50'

        final_list.append(copy.deepcopy(filler_dict))

    return final_list


if __name__ == '__main__':
    print taxi_for_sure_api(28.739137, 77.124717)