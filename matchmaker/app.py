from flask import Flask
from flask import request
import logging
import sys
from flask_cors import CORS
from urllib import parse
import urllib.request
import json
from cupid.cupid import *

app = Flask(__name__)
CORS(app)

static_endpoint = "http://localhost:8080"
@app.route('/')
def hello():
    print(request.environ)
    return request.remote_addr

@app.route('/test/<user_id>')
def test(user_id):
    user_info = {'timeOpened': '2019-03-31T18:37:50.965Z', 'timezone': 4, 'longitude': -80.5327216, 'latitude': 43.4653171, 'heading': None, 'speed': None, 'altitude': None, 'altitudeAccuracy': None, 'timestamp': '2019-03-31T18:37:50.968Z', 'browserName': 'Mozilla', 'referrer': '', 'sizeScreenW': 1920, 'sizeScreenH': 1080, 'browserWidth': 968, 'browserHeight': 918}
    pref_map = [('browserName','Chrome',0), ('timezone',3,1)]
    model = load_model(user_id)
    loss = eval_model(model, user_info, pref_map, 3)
    return "loss: "+str(loss)
    clear_session()

@app.route('/data')
def gatway():
    data = request.args.get('data')
    data = json.loads(data)

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
    
    user_info = {'timeOpened': '2019-03-31T18:37:50.965Z', 'timezone': 4, 'longitude': -80.5327216, 'latitude': 43.4653171, 'heading': None, 'speed': None, 'altitude': None, 'altitudeAccuracy': None, 'timestamp': '2019-03-31T18:37:50.968Z', 'browserName': 'Mozilla', 'referrer': '', 'sizeScreenW': 1920, 'sizeScreenH': 1080, 'browserWidth': 968, 'browserHeight': 918}
    pref_map = [('browserName','Chrome',0), ('timezone',3,1)]

    model, loss = build_model(user_info, pref_map, 3)
    print("loss is ", loss)
    save_model(model)
    clear_session()

    if int(width) < 1000:
        return static_endpoint+"/layouts/view1/"
    elif browser == "Chrome":
        return static_endpoint+"/layouts/view2/"
    else:
        return static_endpoint+"/layouts/view3/"

if __name__ == '__main__':
    app.run(port=3000)
