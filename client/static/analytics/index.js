const express = require('express');
const app = express();
const cors = require('cors');
const port = 5000;

app.use(cors())

var table = {}

app.get('/data', (req, res) => {
  var ip = req.headers['x-forwarded-for'] || 
            req.connection.remoteAddress || 
            req.socket.remoteAddress ||
            (req.connection.socket ? req.connection.socket.remoteAddress : null);
  table[ip] = req.query.data;
})

app.listen(port, () => {})