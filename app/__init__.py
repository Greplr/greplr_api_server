from flask import Flask

app = Flask(__name__, static_url_path='/static')
from app import views
import os

app.config['SECRET_KEY'] = 'thisisarandomstring007becauseilovejamesbond'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = os.getcwd()

#DataWeave key = fe56ada991a6d6d69fb6344bb2189b412bd404e8
