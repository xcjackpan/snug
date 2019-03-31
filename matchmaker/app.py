from flask import Flask
import logging
import sys
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

static_endpoint = "localhost:8080"
@app.route('/')
def hello():
    print("ryan")
    return "Hello World!"

@app.route('/data/<data>')
def data():
    print('alkjdfaldkjfsdlkfjsdlkfjsd')
    print(request.query_string())
    return static_endpoint+'/layouts/view1/'



# app.get('/data', (req, res) => {
#   var data = JSON.parse(req.query.data);
#   var ip = req.headers['x-forwarded-for'] || 
#           req.connection.remoteAddress || 
#           req.socket.remoteAddress ||
#           (req.connection.socket ? req.connection.socket.remoteAddress : null);
#   console.log(ip);
#   console.log(data);
#   if (data["browserWidth"] < 1000) {
#     res.status(200).send(`${clientHost}/view3`);
#   } else if (data["browserName"] === 'Chrome') {
#     res.status(200).send(`${clientHost}/view1`);
#   } else if (data["browserName"] === 'Mozilla') {
#     res.status(200).send(`${clientHost}/view2`);
#   } else {
#     res.status(200).send(`${clientHost}/view2`);
#   }
  
# });


@app.route('/view1')
def view1():
    return static_endpoint+'/layouts/view1/'

@app.route('/view2')
def view2():
    return static_endpoint+'/layouts/view2/'

@app.route('/view3')
def view3():
    return static_endpoint+'/layouts/view3/'

if __name__ == '__main__':
    app.run(port=3000)
