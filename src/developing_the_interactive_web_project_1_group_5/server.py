from flask import Flask, render_template, request, url_for, redirect, g, session 
from functools import wraps
from authlib.integrations.flask_client import OAuth

import os

import developing_the_interactive_web_project_1_group_5.database as database

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

# auth0 setup (can make a new file for auth later, but let's just leave it here for starters)
oauth = OAuth(app)

domain = os.environ["AUTH0_DOMAIN"]
client_id = os.environ["AUTH0_CLIENT_ID"]
client_secret = os.environ["AUTH0_CLIENT_SECRET"]

oauth.register(
    "auth0",
    client_id=client_id,
    client_secret=client_secret,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{domain}/.well-known/openid-configuration'
)

database.setup()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

@login_required
@app.route("/") 
def landing(): 
    if 'user' in session: 
        return "<p>It works</p>"
    else:
        return "<p>User not logged in</p>"

@app.route("/search")
def search():
    return


@app.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Callback redirect from Auth0
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/login")
def login():
    """
    Redirects the user to the Auth0 Universal Login
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/node/<int:node_id>")
def view_node(node_id):
    return

@app.route("/edit-node/<int:node_id>")
def edit_node(node_id):
    return

@app.route("/create-node")
def create_node():
    return

@app.route("/profile/<int:user_id>")
def view_profile(user_id):
    return

@app.route("/edit-profile/<int:user_id>")
def edit_profile(user_id):
    return