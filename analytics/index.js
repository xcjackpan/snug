const express = require('express')
const app = express()
const path = require('path')
const port = 3000
const clientHost = "http://localhost:3000"

app.get('/data', (req, res) => {
  var data = JSON.parse(req.query.data);
  var ip = req.headers['x-forwarded-for'] || 
          req.connection.remoteAddress || 
          req.socket.remoteAddress ||
          (req.connection.socket ? req.connection.socket.remoteAddress : null);
  console.log(ip);
  console.log(data);
  if (data["browserWidth"] < 1000) {
    res.status(200).send(`${clientHost}/view3`);
  } else if (data["browserName"] === 'Chrome') {
    res.status(200).send(`${clientHost}/view1`);
  } else if (data["browserName"] === 'Mozilla') {
    res.status(200).send(`${clientHost}/view2`);
  } else {
    res.status(200).send(`${clientHost}/view2`);
  }
  
});

app.get('/view1', (req, res) => {
  res.sendFile(path.join(__dirname, '/layouts/view1/view1.html'))
});

app.get('/view2', (req, res) => {
  res.sendFile(path.join(__dirname, '/layouts/view2/view2.html'))
});

app.get('/view3', (req, res) => {
  res.sendFile(path.join(__dirname, '/layouts/view3/view3.html'))
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '/index.html'))
});

app.listen(port)