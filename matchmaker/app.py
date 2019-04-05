from flask import Flask
from flask import request
import logging
import sys
from flask_cors import CORS
from urllib import parse
import urllib.request
import json


app = Flask(__name__)
CORS(app)

static_endpoint = "http://localhost:8080"
@app.route('/')
def hello():
    print("asdf")
    return "Hello World!"


@app.route('/data')
def gatway():
    data = request.args.get('data')
    data = json.loads(data)
    print(data)
    browser = data["browserName"]
    width = data["browserWidth"]
    ip = request.remote_addr or request.environ['REMOTE_ADDR'] or request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = '24.114.29.182' if ip == '127.0.0.1' else ip
    ipdata_url = ' https://api.ipdata.co/{}?api-key=8126619017ec195ddb6291b648627d54ec58a029e47867530196eb9f'.format(ip)
    country_data = urllib.request.urlopen(ipdata_url).read()
    country_data = json.loads(country_data)
    data['longitude'] = country_data['longitude']
    data['latitude'] = country_data['latitude']
    data['is_canada'] = (country_data['country_code'] == 'CA')
    data['is_us'] = (country_data['country_code'] == 'US')
    
    print(data)
    if int(width) < 1000:
        return static_endpoint+"/layouts/view1/"
    elif browser == "Chrome":
        return static_endpoint+"/layouts/view2/"
    else:
        return static_endpoint+"/layouts/view3/"

if __name__ == '__main__':
    app.run(port=3000)
