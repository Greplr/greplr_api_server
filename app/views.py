#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app

import flask, flask.views
from flask import render_template,request,make_response,redirect,Response, url_for
import json,urllib2,xml,datetime,hashlib,time,requests,base64

from base64 import b64encode
import requests
import hashlib

from credentials import client_id,client_secret


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

