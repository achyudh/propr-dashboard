from flask import Flask, request, redirect, session, g, flash
from flask_session import Session
from flask.ext.github import GitHub
from jwt import JWT, jwk_from_pem
from requests.auth import HTTPBasicAuth
import requests, json, urllib, pymongo, sys, time, hashlib

app = Flask(__name__)
sess = Session()
with open("config.json", 'r') as config_file:
    client_config = json.load(config_file)
with open("private-key.pem", 'rb') as priv_key_file:
    priv_key = jwk_from_pem(priv_key_file.read())
http_auth_username = client_config['HTTP_AUTH_USERNAME']
http_auth_secret = client_config['HTTP_AUTH_SECRET']
http_auth = HTTPBasicAuth(http_auth_username, http_auth_secret)
app.config['SESSION_TYPE'] = 'mongodb'
app.config['GITHUB_CLIENT_ID'] = client_config['GITHUB_CLIENT_ID']
app.config['GITHUB_CLIENT_SECRET'] = client_config['GITHUB_CLIENT_SECRET']
sess.init_app(app)
github = GitHub(app)





if __name__ == '__main__':
    app.run(threaded=True)
