'use strict';

const request = require('request');
const express = require('express');
let accessToken;

require('./gAuth.js')(function (error,tokens){
    if (error) 
        console.log("Error making request to generate access token:", error);
    else if (tokens.access_token === null)
        console.log("Provided service account does not have permission to generate access tokens");
    else
        accessToken = tokens.access_token;

}.bind(this));


const PORT = 8080;
const HOST = 'localhost';


const app = express();
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello world\n');
});

app.post('/evaluate', (req, res) => {
    var essay = req.body.essay;
    new Promise(function(resolve, reject) {

        const { spawn } = require('child_process');
        const predict = spawn('python3',['prediction.py',essay]);
    
        predict.stdout.on('data', function(data) {
            data = new Buffer.from(data, 'base64').toString("ascii")
            resolve(data);
        });
    
        predict.stderr.on('data', (data) => {
            data = new Buffer.from(data, 'base64').toString("ascii")
            reject(data);
        });
    })
    .then((marks)=>{
        res.send(marks)
    })
    .catch((err)=>{
        console.log(err)
    })
});


app.post('/contribute', (req, res) => {
    var body = req.body;
    var score = body.score;
    var essay = body.essay;
    var prompt = body.prompt;

    var options = {
        uri: `https://softlab-ba722.firebaseio.com/${prompt}/.json`,
        method: 'POST',
        body: {
          "essay": essay,
          "score": score
        },
        headers: {
            "Content-Type":"application/json",
            "Authorization":`Bearer ${accessToken}`
        },
        json: true
    };
    request(options, function(err,response,body){
            res.send("Success");
    })
});

app.get('/:id', (req, res) => {
    var prompt = req.params.id;

    var options = {
        uri: `https://softlab-ba722.firebaseio.com/${prompt}.json`,
        method: 'GET',
        headers: {
            "Content-Type":"application/json",
            "Authorization":`Bearer ${accessToken}`
        },
        json: true
    };
    request(options, function(err,response,body){
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(body, null, 3));
    })
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`)