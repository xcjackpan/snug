from flask import Flask
from flask import request
import logging
import sys
from flask_cors import CORS
from urllib import parse
import ast
import json

app = Flask(__name__)
CORS(app)

static_endpoint = "localhost:8080"
@app.route('/')
def hello():
    print("asdf")
    return "Hello World!"


@app.route('/data')
def gatway():
    data = request.args.get('data')
    data = json.loads(data)
    browser = data["browserName"]
    width = data["browserWidth"]
    ip = request.remote_addr
    print(data)
    if int(width) < 1000:
        return "http://localhost:8080/layouts/view1/"
    elif browser == "Chrome":
        return "http://localhost:8080/layouts/view2/"
    else:
        return "http://localhost:8080/layouts/view3/"

if __name__ == '__main__':
    app.run(port=3000)
