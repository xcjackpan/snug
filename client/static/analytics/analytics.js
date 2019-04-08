var timeOpened = new Date();

var info={
  timeOpened:new Date(),
  timezone:(new Date()).getTimezoneOffset()/60,
  longitude: 0,
  latitude: 0,
};
let browserName = 'unknown browser';
if (navigator.userAgent.includes('Chrome')) browserName = 'Chrome';
else if (navigator.userAgent.includes('Mozilla')) browserName = 'Mozilla';
navigator.geolocation.getCurrentPosition((pos) => {
  info.longitude = pos.coords.longitude;
  info.latitude = pos.coords.latitude;
  info.heading = pos.coords.heading;
  info.speed = pos.coords.speed;
  info.altitude = pos.coords.altitude;
  info.altitudeAccuracy = pos.coords.altitudeAccuracy;
  info.timestamp = new Date(pos.timestamp);
  info.browserName = browserName;
  info.referrer = document.referrer,
  info.sizeScreenW = screen.width;
  info.sizeScreenH = screen.height;
  info.browserWidth = window.innerWidth;
  info.browserHeight = window.innerHeight;
})


window.addEventListener("beforeunload", function(e) {
    var timeNow = new Date();
    info.duration = ((timeNow.getTime() - timeOpened.getTime())/1000 % 60);
    send(info);
})

function send(info) {
  const xhr = new XMLHttpRequest();
  const url='http://localhost:5000/data?data=' + encodeURIComponent(JSON.stringify(info));
  xhr.open("GET", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      window.location.href = xhr.responseText;
    }
  }
  xhr.send();
}