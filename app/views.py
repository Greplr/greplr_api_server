#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
import copy
import flask, flask.views
from flask import render_template,request,make_response,redirect,Response, url_for
import json,urllib2,xml,datetime,hashlib,time,requests,base64
from flask import jsonify
from base64 import b64encode
import requests
import hashlib

from credentials import client_id,client_secret, uber_credentials

from credentials import google_places_api_key
from utils import get_dict,distance
from geopy.distance import vincenty

from flask.ext.httpauth import HTTPBasicAuth

from travel import *


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
    result = {
        'result': []
    }

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

    try:
        list_of_result = uber_api(request.form['latitude'], request.form['longitude'])
        for res in list_of_result:
            result['result'].append(copy.deepcopy(res))
    except:
        pass

    try:
        list_of_result = taxi_for_sure_api(request.form['latitude'], request.form['longitude'])
        for res in list_of_result:
            result['result'].append(copy.deepcopy(res))
    except:
        pass

    return json.dumps(result)


@app.route('/api/food',methods=['GET','POST'])
def foodserver():
    if request.method == 'GET':
        lat = request.args.get('lat')
        long = request.args.get('long')
    else:
        lat = request.form['lat']
        long = request.form['long']
    
    url = '''https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters&key=%s\
        &location=%s,%s\
        &radius=1000\
        &type=bakery|cafe|department_store|food|grocery_or_supermarket'''%(google_places_api_key,lat,long)
    
    results_json = requests.get(url).json()
    arr =[]
    for i in results_json['results']:
        d = get_dict(id=i['place_id'],\
            name=i['name'],\
            address=i['vicinity'],\
            distance=int(vincenty((lat,long),(float(i['geometry']['location']['lat']),float(i['geometry']['location']['lng']))).meters),\
            type=i['types']
            )
        arr.append(d)

    return jsonify(data=arr)
