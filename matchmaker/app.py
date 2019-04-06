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
layout_endpoints = [static_endpoint+"/layouts/view1/", static_endpoint+"/layouts/view2/", static_endpoint+"/layouts/view3/"]

@app.route('/')
def hello():
    print(request.environ)
    return request.remote_addr

@app.route('/test/<user_id>')
def test(user_id):
    user_info = {'timeOpened': '2019-04-06T05:12:54.103Z', 'timezone': 4, 'longitude': -80.554, 'latitude': 43.474, 'timestamp': '2019-04-06T05:12:54.105Z', 'browserName': 'Chrome', 'referrer': 'http://localhost:8080/', 'sizeScreenW': 1920, 'sizeScreenH': 1080, 'browserWidth': 843, 'browserHeight': 430, 'is_canada': True, 'is_us': False}
    pref_map = [('browserName','Mozilla',0), ('timezone',3,1)]
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

    user_info = {}
    for k,v in data.items():
        if v is not None and v is not '':
            user_info[k]=v
    
    print(user_info)
    user_info_sample = {'timeOpened': '2019-04-06T05:12:54.103Z', 'timezone': 1, 'longitude': -80.554, 'latitude': 43.474, 'timestamp': '2019-04-06T05:12:54.105Z', 'browserName': 'Mozilla', 'referrer': 'http://localhost:8080/', 'sizeScreenW': 1920, 'sizeScreenH': 1080, 'browserWidth': 843, 'browserHeight': 430, 'is_canada': True, 'is_us': False}
    pref_map = [('browserName','Chrome',0), ('timezone',4,0)]
    num_layouts = 3
    model, loss = build_model(user_info_sample, pref_map, num_layouts)
    print("loss is ", loss)
    save_model(model)
    processed_data = preprocess(user_info, num_layouts)
    max_layout = 0
    max_val = 0
    for l in range(num_layouts):
        s_dur = model.predict(np.array([processed_data[l]]))
        print("predicted:", s_dur, l)
        if s_dur > max_val:
            max_val = s_dur
            max_layout = l

    clear_session()

    return layout_endpoints[max_layout]


    # if int(width) < 1000:
    #     return static_endpoint+"/layouts/view1/"
    # elif browser == "Chrome":
    #     return static_endpoint+"/layouts/view2/"
    # else:
    #     return static_endpoint+"/layouts/view3/"

if __name__ == '__main__':
    app.run(port=3000)
