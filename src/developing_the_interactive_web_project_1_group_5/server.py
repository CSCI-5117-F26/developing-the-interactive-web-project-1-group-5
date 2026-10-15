from flask import Flask, render_template, request, url_for, redirect, g, session, abort
from functools import wraps
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from developing_the_interactive_web_project_1_group_5.node import format_node_display, dict_get, get_popular_nodes
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
    server_metadata_url=f"https://{domain}/.well-known/openid-configuration",
)

database.setup()


def check_signin():
    if "user" in session:
        return True


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def landing():
    return render_template(
        "landing.html", loggedin=check_signin()
    )  # I will find more efficient way of checking logged in...


@app.route("/search")
@login_required
def search():
    return


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/auth-login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/signup")
def signup():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True), screen_hint="signup"
    )


@app.route("/login")
def login_overlay():
    return render_template("login.html")


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
    node = database.get_node(node_id)
    if ((node == None)):
        abort(404)
    connections = format_node_display(database.get_node_connections(node_id))

    # TODO: How do you get the user_id?
    # saved_nodes = format_node_display(database.get_saved_nodes(user_id))
    # recent_nodes = format_node_display(database.get_recent_nodes(user_id))
    # created_nodes = format_node_display(database.get_user_nodes(user_id))
    return render_template(
        "node_parent.html",
        node_title = dict_get(node, "title", "Untitled"),
        node_img_url = dict_get(node, "img", "../static/img/temp_chungus.png"), 
        node_owner = (database.get_user(dict_get(node, "creatorid", "1"))["username"] or "Quilt"),
        node_description = dict_get(node,"description","None"),
        connections = connections,
        # saved_nodes = saved_nodes,
        # recent_nodes = recent_nodes,
        # created_nodes = created_nodes,
        loggedin=check_signin(),
    )


@app.route("/edit-node/<int:node_id>")
@login_required
def edit_node(node_id):
    node = database.get_node(node_id)
    if ((node == None)):
        abort(404)
    connections = format_node_display(database.get_node_connections(node_id))

    # TODO: How do you get the user_id?
    # saved_nodes = format_node_display(database.get_saved_nodes(user_id))
    # recent_nodes = format_node_display(database.get_recent_nodes(user_id))
    # created_nodes = format_node_display(database.get_user_nodes(user_id))
    return render_template(
        "node_edit.html",
        node_title = dict_get(node, "title", "Untitled"),
        node_img_url = dict_get(node, "img", "../static/img/temp_chungus.png"), 
        node_owner = (database.get_user(dict_get(node, "creatorid", "1"))["username"] or "Quilt"),
        node_description = dict_get(node,"description","None"),
        connections = connections,
        # saved_nodes = saved_nodes,
        # recent_nodes = recent_nodes,
        # created_nodes = created_nodes,
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
        "name": "John Chungus",
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
        "name": "John Chungus",
        "bio": "Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me-",
    }
    return render_template("settings.html", user=user, loggedin=check_signin())


@app.route("/edit-profile/<int:user_id>")
@login_required
def edit_profile(user_id):
    return

# From https://stackoverflow.com/questions/69234307/flask-generate-404-page-if-data-not-found-in-database
@app.errorhandler(404)
def page_404(e):
    return render_template("404.html"), 404