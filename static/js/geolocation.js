// <!-- The sauce for this geolocation: -->
// <!-- http://html5doctor.com/finding-your-position-with-geolocation/-->

if (navigator.geolocation) {
  var timeoutVal = 10 * 1000 * 1000;
  navigator.geolocation.getCurrentPosition(
    displayPosition, 
    displayError
  );
}
// enableHighAccuracy: true, timeout: timeoutVal, maximumAge: 0 
else {
  alert("Geolocation is not supported by this browser");
}

// Create a global variable that we can bind lat/long to
let coordinates;

function displayPosition(position) {
  // this function pulls the lat and long out of position
  var lat = position.coords.latitude; 
  var lng = position.coords.longitude;

  // Put the values in the hidden(?) form
  // In user.html, this fills the visible lat/lng fields in the record form
  $("#lat").attr("value", lat);
  $("#lng").attr("value", lng);
}

function displayError(error) {
  var errors = { 
    1: 'Permission denied',
    2: 'Position unavailable',
    3: 'Request timeout'
  };
  alert("Error: " + errors[error.code]);
}
