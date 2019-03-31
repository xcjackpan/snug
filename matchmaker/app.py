from flask import Flask
from flask import request
import logging
import sys
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

static_endpoint = "localhost:8080"
@app.route('/')
def hello():
    print("asdf",file=sys.stderr)
    return "Hello World!"


@app.route('/data')
def hello_name():
    data = request.args.get('data')
    print("ryan",file=sys.stderr)
    return "Hello! {}".format(request.args.get('data'))

if __name__ == '__main__':
    app.run(port=3000)
