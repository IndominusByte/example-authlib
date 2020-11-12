from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('.env')
oauth = OAuth(config)

redirect_uri_google = "https://b553a103b824.ngrok.io/auth-google"
redirect_uri_facebook = "https://b553a103b824.ngrok.io/auth-facebook"

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='facebook',
    api_base_url='https://graph.facebook.com/v7.0/',
    access_token_url='https://graph.facebook.com/v7.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v7.0/dialog/oauth',
    client_kwargs={'scope': 'email public_profile'},
)

@app.get('/')
async def homepage(request: Request):
    return HTMLResponse('<a href="/login-google">login google</a><br><br><a href="/login-facebook">login facebook</a>')

@app.get('/login-google')
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, redirect_uri_google)

@app.get('/auth-google')
async def auth_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return dict(user)

@app.get('/login-facebook')
async def login_facebook(request: Request):
    return await oauth.facebook.authorize_redirect(request, redirect_uri_facebook)

@app.get('/auth-facebook')
async def auth_facebook(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    user = await oauth.facebook.get('me?fields=name,email,picture',token=token)
    return user.json()
