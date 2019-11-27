var {google} = require("googleapis");
var serviceAccount = require('./serviceKey.json');

var scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
  ];
  
  var jwtClient = new google.auth.JWT(
    serviceAccount.client_email,
    null,
    serviceAccount.private_key,
    scopes
  );
  

module.exports = function (callback) {
  jwtClient.authorize(function(error, tokens) {
    callback(error, tokens);
  })
};