from flask import Flask, render_template, request, url_for, redirect, g, session
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode

import os

import developing_the_interactive_web_project_1_group_5.database as database

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

oauth = OAuth(app)
csrf = CSRFProtect(app)

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
    server_metadata_url=f"https://{domain}/.well-known/openid-configuration",
)

database.setup()


def check_signin():
    return "sub_id" in session


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_signin():
            return redirect("/login")
        else: 
            return f(*args, **kwargs)
    return decorated


@app.route("/")
def landing():
    return render_template(
        "landing.html", loggedin=check_signin()
    )  


@app.route("/search")
@login_required
def search():
    return


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    sub_id = token.get("userinfo").get('sub')
    session["sub_id"] = sub_id

    if (database.get_user(session.get('sub_id')) == None):
        return redirect("/set-username")
    else:
        return redirect("/")


@app.route("/auth-login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# TODO: Change this to JS modal instead of Jinja template 
@app.route("/login")
def login_overlay():
    return render_template("login.html")


@app.route("/set-username")
@login_required
def set_username():
    if (database.get_user(session.get('sub_id')) == None):
        return render_template("username.html")
    else: 
        return redirect("/")

@app.route("/create-username", methods=["GET", "POST"])
@login_required
def username_setup():
    if (database.get_user(session["sub_id"]) == None):
        username = request.form.get('username')
        database.add_user( subId=session["sub_id"], username=username)
    return redirect("/")


@app.route("/logout")
def logout():
    """
    Logs the user out of the session and from the Auth0 tenant
    """
    session.clear()
    return redirect(
        "https://"
        + domain
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("landing", _external=True),
                "client_id": client_id,
            },
            quote_via=quote_plus,
        )
    )


@app.route("/node/<int:node_id>")
def view_node(node_id):
    # TODO: Replace temporary params with node info from database, fetching using id
    return render_template(
        "node_parent.html",
        node_title="Plate with Alexander and Diogenes",
        node_img_url="../static/img/temp_image.jpg",
        node_owner="Grace",
        node_description="This is a painting of an ornate decorative plate depicting the scene where Alexander meets Diogenes. Created in 1524 by ceramist Master of the Coppa Bergantini.",
        connections=[
            {
                "img_url": "../static/img/temp_con3.jpg",
                "node_title": "Alexander the Great",
                "link": "/node/3",
            },
            {
                "img_url": "../static/img/temp_con2.jpg",
                "node_title": "Plate with Marcus Curtius",
                "link": "/node/2",
            },
            {
                "img_url": "../static/img/temp_con1.jpg",
                "node_title": "Plate with Battle Scene",
                "link": "/node/1",
            },
        ],
        loggedin=check_signin(),
    )


@app.route("/edit-node/<int:node_id>")
@login_required
def edit_node(node_id):
    # TODO: Replace temporary params with node info from database, fetching using id
    return render_template(
        "node_edit.html",
        node_title="Plate with Alexander and Diogenes",
        node_img_url="../static/img/temp_image.jpg",
        node_owner="Grace",
        node_description="This is a painting of an ornate decorative plate depicting the scene where Alexander meets Diogenes. Created in 1524 by ceramist Master of the Coppa Bergantini.",
        connections=[
            {
                "img_url": "../static/img/temp_con3.jpg",
                "node_title": "Alexander the Great",
                "link": "/node/3",
            },
            {
                "img_url": "../static/img/temp_con2.jpg",
                "node_title": "Plate with Marcus Curtius",
                "link": "/node/2",
            },
            {
                "img_url": "../static/img/temp_con1.jpg",
                "node_title": "Plate with Battle Scene",
                "link": "/node/1",
            },
        ],
        loggedin=check_signin(),
    )


@app.route("/create-node")
@login_required
def create_node():
    return render_template("node_create.html", connections=[], loggedin=check_signin())


@app.route("/profile")
@login_required
def view_profile():
    user = {
        "name": database.get_user(session["sub_id"])['username'],
        "bio": "Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me-",
    }
    bogus_nodes_yours = ["Chungus node", "bogus node2", "node node"]
    bogus_nodes_saved = [
        "saved node",
        "hihihihihihi",
        "YIPPPEEEEEE",
        "node4  kg. g jg. glu gy lug ulyflf f y",
    ]
    return render_template(
        "profile.html",
        user=user,
        saved=bogus_nodes_saved,
        yours=bogus_nodes_yours,
        loggedin=check_signin(),
    )


@app.route("/settings")
@login_required
def view_settings():
    user = {
        "name": database.get_user(session["sub_id"])['username'],
        "bio": "Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me-",
    }
    return render_template("settings.html", user=user, loggedin=check_signin())


@app.route("/edit-profile/<int:user_id>")
@login_required
def edit_profile(user_id):
    return
