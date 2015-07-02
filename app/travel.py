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
                try:
                    filler_dictionary['product_id'] = y_data['product_id']
                except:
                    filler_dictionary['product_id'] = ''

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
        try:
            filler_dict['product_id'] = res['product_id']
        except:
            filler_dict['product_id'] = ''

        final_list.append(copy.deepcopy(filler_dict))

    return final_list


def goibibo_api(src, dest, day):

    url = 'http://developer.goibibo.com/api/bus/search/?app_id=3d427fd7&app_key=f6b88b898c2059604e9b26e5cf2fee7d&format=json'

    params = {
        'source': src,
        'destination': dest,
        'dateofdeparture': day,
    }

    data = requests.get(url, params=params)

    result_list = []
    filler_dict = {}

    res = data.json()

    print len(res['data']['onwardflights'])

    for x in res['data']['onwardflights']:
        filler_dict['origin'] = x['origin']
        filler_dict['destination'] = x['destination']
        filler_dict['seat'] = x['seat']
        filler_dict['duration'] = x['duration']
        filler_dict['condition'] = x['busCondition']
        filler_dict['fare'] = x['fare']['totalfare']
        filler_dict['bustype'] = x['BusType']
        filler_dict['travelagency'] = x['TravelsName']
        filler_dict['arrdate'] = x['arrdate']
        filler_dict['depdate'] = x['depdate']

        result_list.append(copy.deepcopy(filler_dict))

    return result_list

data_code = {"hyderabad": "HYD", "madurai": "IXM", "hubli": "HBX", "coimbatore": "CJB", "rae bareli": "BEK", "agartala": "IXA", "jamshedpur": "IXW", "daman": "NMB", "calcutta (kolkata)": "CCU", "varanasi": "VNS", "ludhiana": "LUH", "agra": "AGR", "vishakhapatnam": "VTZ", "new delhi": "DEL", "pondicherry": "PNY", "ranchi": "IXR", "bhavnagar": "BHU", "jamnagar": "JGA", "bagdogra": "IXB", "goa": "GOI", "vadodara": "BDQ", "amritsar": "ATQ", "kanpur": "KNU", "patna": "PAT", "silchar": "IXS", "shillong": "SHL", "udaipur": "UDR", "gauhati": "GAU", "dimapur": "DMU", "bhopal": "BHO", "tezpur": "TEZ", "chandigarh": "IXC", "vijayawada": "VGA", "khajuraho": "HJR", "dibrugarh": "DIB", "tirupati": "TIR", "jammu": "IXJ", "leh": "IXL", "poona (pune)": "PNQ", "jodhpur": "JDH", "dehradun": "DED", "port blair": "IXZ", "jorhat": "JRH", "nasik": "ISK", "trivandrum": "TRV", "allahabad": "IXD", "porbandar": "PBD", "tiruchirapally": "TRZ", "aurangabad": "IXU", "bangalore": "BLR", "srinagar": "SXR", "ahmedabad": "AMD", "bhubaneswar": "BBI", "cochin": "COK", "indore": "IDR", "lucknow": "LKO", "mumbai (bombay)": "BOM", "surat": "STV", "chennai(madras)": "MAA", "jaipur": "JAI", "nagpur": "NAG", "gwalior": "GWL", "kozhikode (calicut)": "CCJ", "bhuj": "BHJ", "nanded": "NDC", "diu": "DIU", "rajkot": "RAJ", "imphal": "IMF", "mangalore": "IXE", "puttaparthi": "PUT"}

def goibibo_flight(src, dest, date, num):

    url = 'http://developer.goibibo.com/api/search/?app_id=3d427fd7&app_key=f6b88b898c2059604e9b26e5cf2fee7d'

    '''try:
        source = data_code[src.lower()]
        destination = data_code[dest.lower()]
    except:
        return []'''

    params = {
        'infants': '0',
        'adults': num,
        'children': '0',
        'seatingclass': 'E',
        'dateofdeparture': date,
        'destination': dest,
        'source': src,
        'format': 'json',
    }

    data = requests.get(url, params=params)

    res = data.json()

    result_list = []
    filler_dict = {}

    for x in res['data']['onwardflights']:
        filler_dict['origin'] = x['origin']
        filler_dict['fare'] = x['fare']['totalfare']
        filler_dict['destination'] = x['destination']
        filler_dict['duration'] = x['duration']
        filler_dict['flightnum'] = x['flightno']
        filler_dict['seatingclass'] = x['seatingclass']
        filler_dict['warnings'] = x['warnings']
        filler_dict['airline'] = x['airline']
        filler_dict['depdate'] = x['depdate']
        filler_dict['arrdate'] = x['arrdate']

        result_list.append(copy.deepcopy(filler_dict))

    return result_list

if __name__ == '__main__':
    print taxi_for_sure_api(28.739137, 77.124717)


