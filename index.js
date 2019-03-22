const express = require('express')
const app = express()
const path = require('path')
const port = 3000

app.get('/data', (req, res) => {
  var data = JSON.parse(req.query.data);
  if (data["timezone"] == 4) {
    res.status(200).send("http://xcjackpan.me");
  } else {
    res.status(200).send("httP://ryan-qiyu-jiang.github.io");
  }
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '/index.html'))
});

app.listen(port)