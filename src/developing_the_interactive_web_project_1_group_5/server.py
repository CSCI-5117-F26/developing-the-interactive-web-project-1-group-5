from flask import Flask, render_template, request, url_for, redirect, g, session, abort
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from developing_the_interactive_web_project_1_group_5.node import (
    format_node_display,
    dict_get,
    get_popular_nodes,
)

from psycopg import errors

import os
import developing_the_interactive_web_project_1_group_5.full_text_search as fulltext
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
    categories = format_node_display(database.get_all_categories())
    popular_nodes = format_node_display(get_popular_nodes())


    recent_nodes = format_node_display(database.get_recent_nodes(session.get('sub_id')))
    # new_nodes = format_node_display(database.get_new_nodes??(session.get('sub_id')))
    return render_template(
        "landing.html",
        # categories=categories,
        # popular_nodes=popular_nodes,
        # recent_nodes=recent_nodes,
        # # new_nodes = new_nodes,
        loggedin=check_signin(),
    )


@app.route("/search", methods=["POST"])
@login_required
def search():
    query = request.form["search"]
    parse_query = fulltext.full_text_search(query)
    print(parse_query)
    return render_template("search.html", show=parse_query)


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    sub_id = token.get("userinfo").get("sub")
    session["sub_id"] = sub_id

    if database.get_user(session.get("sub_id")) == None:
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
    if database.get_user(session.get("sub_id")) == None:
        return render_template("username.html")
    else:
        return redirect("/")


@app.route("/create-username", methods=["GET", "POST"])
@login_required
def username_setup():
    if database.get_user(session.get("sub_id")) == None:
        # TODO: Validate username here
        username = request.form.get("username")
        database.add_user(subId=session.get("sub_id"), username=username)
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
    node = database.get_node(node_id)
    if node == None:
        abort(404)
    connections = format_node_display(database.get_node_connections(node_id))


    saved_nodes = format_node_display(database.get_saved_nodes(session.get('sub_id')))
    recent_nodes = format_node_display(database.get_recent_nodes(session.get('sub_id')))
    created_nodes = format_node_display(database.get_user_nodes(session.get('sub_id')))
    return render_template(
        "node_parent.html",
        node_title = dict_get(node, "title", "Untitled"),
        node_img_url = dict_get(node, "img", "../static/img/temp_chungus.png"), 
        # fix this line
        node_owner = (database.get_user(dict_get(node, "subId", "noid"))["username"] or "Quilt"),
        node_description = dict_get(node,"description","None"),
        connections = connections,
        saved_nodes = saved_nodes,
        recent_nodes = recent_nodes,
        created_nodes = created_nodes,
        loggedin=check_signin(),
    )


@app.route("/edit-node/<int:node_id>")
@login_required
def edit_node(node_id):
    node = database.get_node(node_id)
    if node == None:
        abort(404)
    connections = format_node_display(database.get_node_connections(node_id))

    # TODO: Change this when you can ge session.get('sub_id')
    
    saved_nodes = format_node_display(database.get_saved_nodes(session.get('sub_id')))
    recent_nodes = format_node_display(database.get_recent_nodes(session.get('sub_id')))
    created_nodes = format_node_display(database.get_user_nodes(session.get('sub_id')))
    return render_template(
        "node_edit.html",
        node_title = dict_get(node, "title", "Untitled"),
        node_img_url = dict_get(node, "img", "../static/img/temp_chungus.png"), 
        node_owner = (database.get_user(dict_get(node, "creatorId", "noid"))["username"] or "Quilt"),
        node_description = dict_get(node,"description","None"),
        connections = connections,
        saved_nodes = saved_nodes,
        recent_nodes = recent_nodes,
        created_nodes = created_nodes,
        loggedin=check_signin(),
    )


@app.route("/create-node", methods=["GET", "POST"])
@login_required
def create_node():
    return render_template("node_create.html", connections=[], loggedin=check_signin())


@app.route("/profile")
@login_required
def view_profile():
    user = {
        "name": database.get_user(session.get("sub_id"))["username"],
        "bio": "Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me-",
    }
    # TODO: Change this when you can get user id from auth
    
    saved_nodes = format_node_display(database.get_saved_nodes(session.get('sub_id')))
    created_nodes = format_node_display(database.get_user_nodes(session.get('sub_id')))
    return render_template(
        "profile.html",
        user=user,
        saved_nodes=saved_nodes,
        created_nodes=created_nodes,
        loggedin=check_signin(),
    )


@app.route("/settings")
@login_required
def view_settings():
    user = {
        "name": database.get_user(session.get("sub_id"))["username"],
        "bio": "Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me crazy. Crazy? I was crazy once. They locked me in a room. A rubber room. A rubber room with rats. And rats make me-",
    }
    return render_template("settings.html", user=user, loggedin=check_signin())


@app.route("/edit-profile/<int:session.get('sub_id')>")
@login_required
def edit_profile():
    return



# From https://stackoverflow.com/questions/69234307/flask-generate-404-page-if-data-not-found-in-database
@app.errorhandler(404)
def page_404(e):
    return render_template("404.html"), 404
