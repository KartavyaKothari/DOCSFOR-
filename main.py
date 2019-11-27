from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from starlette.applications import Starlette
from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse, PlainTextResponse
from prediction import predict
import uvicorn
import json
import requests
import os

scopes = [
  "https://www.googleapis.com/auth/userinfo.email",
  "https://www.googleapis.com/auth/firebase.database"
]
templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
credentials = service_account.Credentials.from_service_account_file("./serviceKey.json", scopes=scopes)
authed_session = AuthorizedSession(credentials)

@app.route('/auth')
async def show_index(request):
    """
        The function is a controller. It is invoked when we call ``/auth``
    """
    return templates.TemplateResponse('index.html', {'request': request})

@app.route('/auth',methods=["POST"])
async def firebase_login(request):
    """
        This function deals with authentication in the code

        :param: request
        :rtype: Templating engine for Python3 rendering

            >>> cool@cool.com and coolcool
            
    """
    body = await request.form()
    email = body['email']
    password = body['password']

    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyBrnRxGfzyWvLZu9XMUnbZTPpu8NxHBRE0"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    response = requests.post(request_ref, headers=headers, data=data)
 
    if response.status_code!=200:
        try:
            message = json.loads(response._content)['error']['message']
        except:
            message = "Some error Occured."
        return templates.TemplateResponse('login.html', {'request': request, 'err_msg':message})
    else:
        return templates.TemplateResponse('index.html', {'request': request})


@app.route('/registration',methods=["POST"])
async def firebase_register(request):
    """
        This function registers us on the firebase platform.

        It accepts user input from UI, ie. The email and password

        The route for the same would be ``@app.route('/registration',methods=["POST"])``
    """

    body = await request.form()
    email = body['email']
    password = body['pass1']
    confirm = body['pass2']

    if password!=confirm:
        message = 'Password do not match.'
        return templates.TemplateResponse('register.html', {'request': request, 'err_msg':message})

    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyBrnRxGfzyWvLZu9XMUnbZTPpu8NxHBRE0"
    headers = {"content-type": "application/json; charset=UTF-8" }
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    response = requests.post(request_ref, headers=headers, data=data)

    if response.status_code!=200:
        try:
            message = json.loads(response._content)['error']['message']
        except:
            message = '<div class="alert alert-danger" role="alert">'+"Some error Occured."+"</div>"
        return templates.TemplateResponse('register.html', {'request': request, 'err_msg':message})
    else:
        message = "Successfully registered."
        return templates.TemplateResponse('login.html', {'request': request, 'err_msg':message})

@app.route('/')
async def login(request):
    """
        This function ensure that whenever we request the url, we are returned to the appropriate chilhood
    """

    message = ''
    return templates.TemplateResponse('login.html', {'request': request,'err_msg':message})

@app.route('/register')
async def login(request):
    """
        For the controller Login, we have two different routes

        1) ``@app.route('/')``, This is invoked when we have a redirect to and from the default start state or direct home href links

        2) ``@app.route('/register')`` We get here when it's the login link vi
        This function gives us the ability of logging in if our username and pass match
    """
    message = ''
    return templates.TemplateResponse('register.html', {'request': request,'err_msg':message})

@app.route('/contribute')
async def contrbPage(request):
    """
    This function gives people the option to contribute the essay set and make the model better.

        >>> Essay: Hi, this is the festival of diwali and I like to enjoy it with my friends and pet cow

        >>> Score: 30/100 
    """
    return templates.TemplateResponse('contribute.html', {'request': request})

@app.route('/{prompt}')
async def getEssay(request):
    """
        This function getEssay is here to give us access to the cloud hosted url whenever. We can now check about donated essays till now.
        This controller operates on route ``@app.route('/{prompt}')``
    """
    prompt = request.path_params['prompt']
    response = authed_session.get("https://softlab-ba722.firebaseio.com/"+prompt+".json")
    data = response.json().values()
    return templates.TemplateResponse('topic.html', {'request': request,'essayResponse':data,'topic':prompt})

@app.route('/evaluateFile',methods=["POST"])
async def evaluateFile(request):
    """
            This funicton gives us a method to get the text out of file directly. Intead of writing text, it is better to upload text.
            
            We see the function on a route ``@app.route('/evaluateFile',methods=["POST"])``
    """
    body = await request.form()
    contents = await body["essayFile"].read()
    contents = contents.decode('utf-8')
    score = predict(contents)
    score = round(float(score)/60*100,2)
    return templates.TemplateResponse('score.html', {'request': request, 'score':score})

@app.route('/evaluate',methods=["POST"])
async def evaluate(request):
    """
    The function finds out the score of a particular essay which was passed to it
    """
    body = await request.form()
    score = predict(body['essay'])
    score = round(float(score)/60*100,2)
    return templates.TemplateResponse('score.html', {'request': request, 'score':score})

@app.route('/contribute',methods=["POST"])
async def evaluate(request):
    """     
        The function evaluate: stores the user input essay and corresponding score
        We have two calls of function evaluate with the distinction of the routes with totally different route.

        1) ``@app.route('/evaluate',methods=["POST"])``
            This sends the essay to the server and recieves the score after some calculation.
        2) ``@app.route('/contribute',methods=["POST"])``
            This is to store the essay and score pair provided by the user and appreciate the wholsomeness of it
    """
    body = await request.form()
    score, essay, prompt = body['score'], body['essay'], body['prompt']
    # score = float(score)/100
    json = { 
        "essay": essay,
        "score": score
    }
    message = "Success, Thanks for your invaluable contribution!"
    response = authed_session.post("https://softlab-ba722.firebaseio.com/"+prompt+"/.json",None,json)
    
    if response.status_code!=200:
        message = "Oops some error occured please try after some time."
    return templates.TemplateResponse('thanks.html', {'request': request, 'score':score, 'message':message, 'essay':essay})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host='0.0.0.0', port=port)