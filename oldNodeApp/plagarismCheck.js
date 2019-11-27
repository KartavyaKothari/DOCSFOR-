var request = require('request');
var CopyleaksCloud = require('plagiarism-checker');
var _ = require('lodash');
var clCloud = new CopyleaksCloud();
var config = clCloud.getConfig();

var credentials = {
    "Email": "sjain0615@gmail.com",
    "ApiKey": "89893811-8da7-432b-8f40-7d4eb6456693"
}

let access_token;

var essay = 'yes i am on moonlight. yes i am on moonlight yes .i am on moonlight yes i am on moonlightyes i am on moonlight. yes i am on moonlight. yes i am on moonlight';

clCloud.login(credentials.Email,credentials.ApiKey,'education',function(resp,err){
    if(!err){
        access_token = _.get(resp,'access_token','');
        console.log(resp);
        var _customHeaders = {};
        _customHeaders[config.SANDBOX_MODE_HEADER] = true; // Sandbox mode - Scan without consuming any credits and get back dummy results
        _customHeaders[config.HTTP_CALLBACK] = 'http://requestb.in/callbacks/' // Callback url - For a fast testing of callbacks option we recommend to use http://requestb.in
        
        clCloud.createByText(essay,_customHeaders,function(resp,err){
            console.log(resp)
            if(resp && resp.ProcessId){
                let PID = resp.ProcessId
                let Status = 'Processing'
                clCloud.getProcessStatus(PID,function(resp,err){
                    console.log(resp.Status,resp)
                    if(resp.Status==='Finished'){
                        clCloud.getProcessResults(PID,function(resp,err){
                        console.log(resp);
                        setTimeout(function(){
                            })
                        },15);


                    }
                    else{
                        clCloud.getProcessResults(PID,function(resp,err){
                        console.log(resp.results);
                        setTimeout(function(){

                        },15);
                        })
                    }
                })
            }
        }); 
    }
})

// var pid = '4decf855-60d6-4b9e-985b-4bfcfdb6bd63'


// function setToken(){

//     var headers = {
//         "Content-type": "application/json"
//     };
    

    
//     var options = {
//         url: "https://id.copyleaks.com/v1/account/login-api",
//         method: "POST",
//         headers: headers,
//         body: dataString,
//         json: true
//     };
    
//     return new Promise(function(resolve,reject){
//         clCloud.login(options, function(error, response, body) {
//             if (!error && response.statusCode == 200)
//                 resolve(body.access_token)
//             else
//                 reject(error)
//         })
//     })
// }

// function scanFile(token, essay){

//     var headers = {
//         'Authorization': `Bearer ${token}`,
//         'Content-type': "application/json"
//     };

    
//     var options = {
//         url: "https://id.copyleaks.com/v2/education/4d7728fb-ed3e-4c77-8a2c-07783cfad046/result",
//         method: "GET",
//         headers: headers,
//         body: essay
//     };

//     request(options,function(error, response, body) {
//         if (!error && response.statusCode == 200) {
//             console.log(body);
//         }
//     });
// }

// setToken()
// .then((token)=>{
//     scanFile(token,essay)
// })
// .catch((err)=>console.log('err '+err))
