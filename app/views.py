#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import urllib2
import xml
import datetime
import hashlib
import time
import base64
from base64 import b64encode
import hashlib

import flask
import flask.views
from flask import render_template, request, make_response, redirect, Response, url_for
import requests
from flask import jsonify
import requests
from geopy.distance import vincenty
from flask.ext.httpauth import HTTPBasicAuth
import sendgrid
from bs4 import BeautifulSoup as BS

from app import app
from models import Feedback, Subscribe, Contact
from credentials import client_id, client_secret, uber_credentials, parse_credentials
from credentials import google_places_api_key
from utils import get_dict, distance
from travel import *
from food import *
from shop import *
from food_mmx import *
from events import *

auth = HTTPBasicAuth()

users = {
    "admin": "kuchbhi123"
}


############################################CACHING##############################################

@app.after_request
def cache(response):
    # response.cache_control.max_age = 60
    response.headers['Cache-Control'] = 'public, max-age=60, only-if-cached, max-stale=0'
    return response


#################################################################################################

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route('/api')
def apiserver():
    return "fooo"


@app.route('/georev', methods=['GET'])
def reverse_geocode():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')

    url = 'https://api.mapmyindia.com/v3?fun=rev_geocode&lic_key=wnnpaidz5ghljto6wupj1k3p3xmcry21&lng=' + str(
        lon) + '&lat=' + str(lat)

    data = requests.get(url)

    listData = data.json()
    return data.text


@app.route('/geo', methods=['GET'])
def geocoding():
    query = request.args.get('location')

    url = 'https://api.mapmyindia.com/v3?fun=geocode&lic_key=wnnpaidz5ghljto6wupj1k3p3xmcry21&q=' + str(query)

    data = requests.get(url)

    listData = data.json()
    return data.text


@app.route('/api/travel/cabs', methods=['GET', 'GET'])
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
        list_of_result = uber_api(request.args.get('lat'), request.args.get('lng'))
        for res in list_of_result:
            result.append(copy.deepcopy(res))
    except:
        pass

    try:
        list_of_result = taxi_for_sure_api(request.args.get('lat'), request.args.get('lng'))
        for res in list_of_result:
            result.append(copy.deepcopy(res))
    except:
        pass

    final_result = sorted(result, key=lambda k: k['time_of_arrival'])

    return json.dumps(final_result)


@app.route('/api/travel/bus', methods=['GET'])
def travel_bus():
    src = request.args.get('src')
    dest = request.args.get('dest')
    date_leave = request.args.get('date')

    x = date_leave.split('-')
    date = x[2] + x[1] + x[0]

    result = goibibo_api(src, dest, date)

    return json.dumps(result)


@app.route('/api/travel/flight', methods=['GET'])
def travel_flight():
    src = request.args.get('src')
    dest = request.args.get('dest')
    date = request.args.get('date')
    num = request.args.get('adults')

    x = date.split('-')
    date = x[2] + x[1] + x[0]

    result = goibibo_flight(src, dest, date, num)

    return json.dumps(result)


@app.route('/api/food/order', methods=['GET'])
def foodpanda_order():
    try:
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        return foodpanda(lat=lat, lng=lng)
    except:
        id = request.args.get('id')
        return foodpanda(id=id)


@app.route('/api/food/restaurants', methods=['GET'])
def food_restaurant():
    lat = request.args.get('lat')
    long = request.args.get('lng')

    url = '''https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters&key=%s\
        &location=%s,%s\
        &radius=2000\
        &type=food|restaurant''' % (google_places_api_key, lat, long)

    results_json = requests.get(url).json()
    # print results_json
    arr = []
    for i in results_json['results']:
        d = get_dict(id=i['place_id'], \
                     name=i['name'], \
                     address=i['vicinity'], \
                     distance=int(vincenty((lat, long), (
                     float(i['geometry']['location']['lat']), float(i['geometry']['location']['lng']))).meters), \
                     type=i['types'],
                     lat=i['geometry']['location']['lat'],
                     lng=i['geometry']['location']['lng']
                     )
        try:
            d['rating'] = i['rating']
        except:
            d['rating'] = '0.0'

        try:
            d['open_now'] = i['opening_hours']['open_now']
        except:
            d['open_now'] = 'no response'
        arr.append(copy.deepcopy(d))

    return json.dumps(arr)


@app.route('/api/food/bar', methods=['GET'])
def food_bar():
    lat = request.args.get('lat')
    long = request.args.get('lng')

    url = '''https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters&key=%s\
        &location=%s,%s\
        &radius=2000\
        &type=bar''' % (google_places_api_key, lat, long)

    results_json = requests.get(url).json()
    arr = []
    for i in results_json['results']:
        d = get_dict(id=i['place_id'], \
                     name=i['name'], \
                     address=i['vicinity'], \
                     distance=int(vincenty((lat, long), (
                     float(i['geometry']['location']['lat']), float(i['geometry']['location']['lng']))).meters), \
                     type=i['types'],
                     lat=i['geometry']['location']['lat'],
                     lng=i['geometry']['location']['lng']
                     )
        try:
            d['rating'] = i['rating']
        except:
            d['rating'] = '0.0'

        try:
            d['open_now'] = i['opening_hours']['open_now']
        except:
            d['open_now'] = 'no response'
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

    return float(res.json()['aggregate']['score']) * 5.0


@app.route('/api/food/cafe', methods=['GET'])
def food_cafe():
    lat = request.args.get('lat')
    long = request.args.get('lng')

    url = '''https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters&key=%s\
        &location=%s,%s\
        &radius=2000\
        &type=cafe''' % (google_places_api_key, lat, long)

    results_json = requests.get(url).json()
    arr = []
    for i in results_json['results']:
        d = get_dict(id=i['place_id'], \
                     name=i['name'], \
                     address=i['vicinity'], \
                     distance=int(vincenty((lat, long), (
                     float(i['geometry']['location']['lat']), float(i['geometry']['location']['lng']))).meters), \
                     type=i['types'],
                     lat=i['geometry']['location']['lat'],
                     lng=i['geometry']['location']['lng']
                     )
        try:
            d['rating'] = i['rating']
        except:
            d['rating'] = '0.0'
        try:
            d['open_now'] = i['opening_hours']['open_now']
        except:
            d['open_now'] = 'no response'
        arr.append(copy.deepcopy(d))

    return json.dumps(arr)


@app.route('/api/events/movies', methods=['GET'])
def movies():

    arr = []

    try:
        arr += events_movies()
    except:
        pass

    return json.dumps(arr)


@app.route('/api/events/plays', methods=['GET'])
def plays():

    arr = []

    try:
        arr += events_plays()
    except:
        pass

    return json.dumps(arr)


@app.route('/api/events/concerts', methods=['GET'])
def concerts():

    arr = []

    try:
        arr += events_concerts()
    except:
        pass

    return json.dumps(arr)


@app.route('/api/shop/offers', methods=['GET'])
def offers():
    res = []

    try:
        res += flipkart_offers()
    except:
        pass

    return json.dumps(res)


@app.route('/api/shop/search', methods=['GET'])
def search_items():
    try:
        query = request.args.get('q')
    except:
        query = 'laptop'

    res = []

    try:
        res += flipkart_search(query)
    except:
        pass

    return json.dumps(res)


@app.route('/api/foodmmx/nearme', methods=['GET'])
def for_mmx():
    try:
        lat = str(request.args.get('lat'))
        lng = str(request.args.get('lng'))
    except:
        lat = '28.734371'
        lng = '77.1197519'

    return food_mmx(lat, lng)


@app.route('/api/foodmmx/details', methods=['GET'])
def detailsRestaurant():
    try:
        res = restaurant_details(str(request.args.get('id')))
    except:
        res = {}

    return res


@app.route('/mail/subscribe', methods=['GET'])
def subscribe():
    try:
        email = request.args.get('email')
        sg = sendgrid.SendGridClient('shubham1810', 'shubhamgreplr2015')

        msg = sendgrid.Mail()
        msg.add_to(email)
        msg.set_subject('Subscription of Greplr')
        msg.set_html('''Hi!\n \
                     Thank you for subscribing to Greplr. We will keep you updated about all the changes happening to Greplr.\n \
                     Regards\n \
                     Team Greplr''')
        msg.set_text('Greplr')
        msg.set_from('hi@greplr.com')
        status, mg = sg.send(msg)

        try:
            mail = Subscribe.Query.get(email=email)
        except:
            a = Subscribe(email=email, subscribed_for='alpha')
            a.save()

        return json.dumps('[{\'status\':\'Sent\'}]')

    except:
        return json.dumps('[{\'status\':\'Failed\'}]')


@app.route('/mail/contactus', methods=['GET'])
def contactus():
    try:
        email = request.args.get('email')
        name = request.args.get('name')
        message = request.args.get('message')
        sg = sendgrid.SendGridClient('shubham1810', 'shubhamgreplr2015')

        msg = sendgrid.Mail()
        msg.add_to('hi@greplr.com')
        msg.set_subject('User message')
        msg.set_html(message)
        msg.set_text('Greplr')
        msg.set_from(email)
        status, mg = sg.send(msg)

        return json.dumps('[{\'status\':\'Sent\'}]')

    except:
        return json.dumps('[{\'status\':\'Failed\'}]')
