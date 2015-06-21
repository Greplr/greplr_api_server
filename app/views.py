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
from models import Feedback
from credentials import client_id,client_secret, uber_credentials, parse_credentials

from credentials import google_places_api_key
from utils import get_dict,distance
from geopy.distance import vincenty

from flask.ext.httpauth import HTTPBasicAuth

from travel import *
from food import *


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


@app.route('/georev', methods=['POST'])
def reverse_geocode():
    lat = request.form['latitude']
    lon = request.form['longitude']

    url = 'https://api.mapmyindia.com/v3?fun=rev_geocode&lic_key=wnnpaidz5ghljto6wupj1k3p3xmcry21&lng='+str(lon)+'&lat='+str(lat)

    data = requests.get(url)

    listData = data.json()
    return data.text

@app.route('/geo', methods=['POST'])
def geocoding():
    query = request.form['location']

    url = 'https://api.mapmyindia.com/v3?fun=geocode&lic_key=wnnpaidz5ghljto6wupj1k3p3xmcry21&q='+str(query)

    data = requests.get(url)

    listData = data.json()
    return data.text

@app.route('/api/travel/cabs', methods=['GET', 'POST'])
def travel_api():
    result = []

    ''' ========================Example JSON to be sent===============
    result = [
            {
                'provider': 'provider_name',
                'time_of_arrival': 'time in minutes',
                'price_per_km': 'price in INR/Km',
                'display_name': 'Black/X/GO',
                'min_price': 'minimum_price',
            },
        ]
    =============================================================='''

    try:
        list_of_result = uber_api(request.form['lat'], request.form['lng'])
        for res in list_of_result:
            result.append(copy.deepcopy(res))
    except:
        pass

    try:
        list_of_result = taxi_for_sure_api(request.form['lat'], request.form['lng'])
        for res in list_of_result:
            result.append(copy.deepcopy(res))
    except:
        pass

    return json.dumps(result)


@app.route('/api/travel/bus', methods=['POST'])
def travel_bus():

    src = request.form['src']
    dest = request.form['dest']
    date_leave = request.form['date']

    result = goibibo_api(src, dest, date_leave)

    return json.dumps(result)

@app.route('/api/travel/flight', methods=['POST'])
def travel_flight():

    src = request.form['src']
    dest = request.form['dest']
    date = request.form['date']
    num = request.form['adults']

    result = goibibo_flight(src, dest, date, num)

    return json.dumps(result)

@app.route('/api/food/restaurants', methods=['POST'])
def food_restaurant():
    lat = request.form['lat']
    long = request.form['lng']

    url = '''https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters&key=%s\
        &location=%s,%s\
        &radius=1000\
        &type=department_store|food|grocery_or_supermarket''' %(google_places_api_key,lat,long)

    results_json = requests.get(url).json()
    print results_json
    arr =[]
    for i in results_json['results']:
        d = get_dict(id=i['place_id'],\
            name=i['name'],\
            address=i['vicinity'],\
            distance=int(vincenty((lat,long),(float(i['geometry']['location']['lat']),float(i['geometry']['location']['lng']))).meters),\
            type=i['types'],
            lat = i['geometry']['location']['lat'],
            lng = i['geometry']['location']['lng']
            )
        arr.append(copy.deepcopy(d))

    return json.dumps(arr)


@app.route('/api/food/bar', methods=['POST'])
def food_bar():
    lat = request.form['lat']
    long = request.form['lng']

    url = '''https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters&key=%s\
        &location=%s,%s\
        &radius=1000\
        &type=bar''' %(google_places_api_key,lat,long)

    results_json = requests.get(url).json()
    arr =[]
    for i in results_json['results']:
        d = get_dict(id=i['place_id'],\
            name=i['name'],\
            address=i['vicinity'],\
            distance=int(vincenty((lat,long),(float(i['geometry']['location']['lat']),float(i['geometry']['location']['lng']))).meters),\
            type=i['types'],
            lat = i['geometry']['location']['lat'],
            lng = i['geometry']['location']['lng']
            )
        arr.append(copy.deepcopy(d))

    return json.dumps(arr)


@app.route('/api/feedback', methods=['POST'])
def feedback():
    feed = request.form['feedback']
    user = request.form['user']
    field = request.form['field']

    senti = sentiment(feed)

    u = Feedback(user=user, feed=feed, field=field, rating=senti)
    u.save()

    return json.dumps([{'status': 'done'}])


def sentiment(data):

    url = 'https://api.idolondemand.com/1/api/sync/analyzesentiment/v1'

    params = {
        'apikey': '17485be9-1aa8-42d2-959c-eca724679547',
        'text': data
    }

    res = requests.post(url, data=params)

    return float(res.json()['aggregate']['score'])*5.0


@app.route('/api/food/cafe', methods=['POST'])
def food_cafe():
    lat = request.form['lat']
    long = request.form['lng']

    url = '''https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters&key=%s\
        &location=%s,%s\
        &radius=1000\
        &type=bakery|cafe''' %(google_places_api_key,lat,long)

    results_json = requests.get(url).json()
    arr =[]
    for i in results_json['results']:
        d = get_dict(id=i['place_id'],\
            name=i['name'],\
            address=i['vicinity'],\
            distance=int(vincenty((lat,long),(float(i['geometry']['location']['lat']),float(i['geometry']['location']['lng']))).meters),\
            type=i['types'],
            lat = i['geometry']['location']['lat'],
            lng = i['geometry']['location']['lng']
            )
        arr.append(copy.deepcopy(d))

    return json.dumps(arr)


@app.route('/api/events/movies', methods=['GET'])
def movies():
    url = 'http://data-in.bookmyshow.com/'

    params = {
        'cmd': 'GETEVENTLIST',
        'f': 'json',
        't': '67x1xa33b4x422b361ba',
        'rc': 'NCR',
        'et': 'MT',
    }

    data = requests.get(url, params=params)
    res = data.json()

    result = res['BookMyShow']['arrEvent']

    return json.dumps(result)