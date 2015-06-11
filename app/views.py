#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
import copy
import flask, flask.views
from flask import render_template,request,make_response,redirect,Response, url_for
import json,urllib2,xml,datetime,hashlib,time,requests,base64

from base64 import b64encode
import requests
import hashlib

from credentials import client_id,client_secret, uber_credentials


from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "kuchbhi123"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route('/api')
def apiserver():
    return "fooo"

@app.route('/api/travel', methods=['GET', 'POST'])
def travel_api():
    latitude = request.form['latitude']
    longitude = request.form['longitude']

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

    return json.dumps(result['result'])