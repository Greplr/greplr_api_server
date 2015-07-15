__author__ = 'championswimmer'
import json

import requests

def events_movies():
    url = 'http://data-in.bookmyshow.com/'

    params = {
        'cmd': 'GETEVENTLIST',
        'f': 'json',
        't': '67x1xa33b4x422b361ba',
        'rc': 'NCR',
        'et': 'MT',
        'src': 'GURG',
    }

    data = requests.get(url, params=params)
    res = data.json()

    result = res['BookMyShow']['arrEvent']

    return result

def events_plays():
    url = 'http://data-in.bookmyshow.com/'

    params = {
        'cmd': 'GETEVENTLIST',
        'f': 'json',
        't': '67x1xa33b4x422b361ba',
        'rc': 'NCR',
        'et': 'PL',
        'src': 'GURG',
    }

    data = requests.get(url, params=params)
    res = data.json()

    result = res['BookMyShow']['arrEvent']

    return result

def events_concerts():
    url = 'http://data-in.bookmyshow.com/'

    params = {
        'cmd': 'GETEVENTLIST',
        'f': 'json',
        't': '67x1xa33b4x422b361ba',
        'rc': 'NCR',
        'et': 'CT',
        'src': 'GURG',
    }

    data = requests.get(url, params=params)
    res = data.json()

    result = res['BookMyShow']['arrEvent']

    return result

if __name__ == '__main__':
    pass

