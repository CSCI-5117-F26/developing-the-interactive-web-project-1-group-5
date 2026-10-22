from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    g,
    session,
    abort,
    send_file,
)
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from developing_the_interactive_web_project_1_group_5.node import (
    format_node_display,
    dict_get,
    get_popular_nodes,
)
from developing_the_interactive_web_project_1_group_5.node import (
    format_node_display,
    dict_get,
    get_popular_nodes,
)

from psycopg import errors

import io
import os
import developing_the_interactive_web_project_1_group_5.full_text_search as fulltext
import developing_the_interactive_web_project_1_group_5.full_text_search as fulltext
import datetime
import random
import developing_the_interactive_web_project_1_group_5.database as database

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1000 * 1000
)  # Rejects any kinda upload that'll exceed 5MB. Taken from Flask documentation (Uploading Files, 'Improving Uploads')

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
    recent_nodes = format_node_display(database.get_recent_nodes(session.get("sub_id")))
    # new_nodes = format_node_display(database.get_new_nodes(session.get("sub_id")))

    all_nodes = format_node_display(fulltext.view())
    random_node = random.choice(all_nodes)
    print(random_node)
    return render_template(
        "landing.html",
        categories=categories,
        popular_nodes=popular_nodes,
        recent_nodes=recent_nodes,
        # new_nodes=new_nodes,
        random_node=random_node,
        loggedin=check_signin(),
    )


@app.route("/search", methods=["POST"])
@login_required
def search():
    query = request.form["search"]
    parse_query = format_node_display(fulltext.full_text_search(query))
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
    saved_nodes = format_node_display(database.get_saved_nodes(session.get("sub_id")))
    recent_nodes = format_node_display(database.get_recent_nodes(session.get("sub_id")))
    created_nodes = format_node_display(database.get_user_nodes(session.get("sub_id")))
    return render_template(
        "node_parent.html",
        node_title=dict_get(node, "title", "Untitled"),
        node_img_url=dict_get(node, "img", "../static/img/temp_chungus.png"),
        # fix this line
        node_owner=(
            database.get_user(dict_get(node, "subid", "noid"))["username"] or "Quilt"
        ),
        node_description=dict_get(node, "description", "None"),
        connections=connections,
        saved_nodes=saved_nodes,
        recent_nodes=recent_nodes,
        created_nodes=created_nodes,
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
    saved_nodes = format_node_display(database.get_saved_nodes(session.get("sub_id")))
    recent_nodes = format_node_display(database.get_recent_nodes(session.get("sub_id")))
    created_nodes = format_node_display(database.get_user_nodes(session.get("sub_id")))
    return render_template(
        "node_edit.html",
        node_title=dict_get(node, "title", "Untitled"),
        node_img_url=dict_get(node, "img", "../static/img/temp_chungus.png"),
        node_owner=(
            database.get_user(dict_get(node, "creatorId", "noid"))["username"]
            or "Quilt"
        ),
        node_description=dict_get(node, "description", "None"),
        connections=connections,
        saved_nodes=saved_nodes,
        recent_nodes=recent_nodes,
        created_nodes=created_nodes,
        loggedin=check_signin(),
    )


@app.route("/create-node", methods=["GET", "POST"])
@login_required
def create_node():
    return render_template("node_create.html", connections=[], loggedin=check_signin())

@app.route("/images/<int:image_id>")
def get_image(image_id):
    row = database.get_image(image_id)
    if row == None:
        abort(404)
    return send_file(io.BytesIO(row["data"]), mimetype=row["mimetype"])


@app.route("/profile")
@login_required
def view_profile():
    db_user = database.get_user(session.get("sub_id"))
    user = {
        "name": db_user["username"],
        "bio": db_user.get("bio"),
        "profpicid": db_user.get("profpicid"),
    }

    saved_nodes = format_node_display(database.get_saved_nodes(session.get("sub_id")))
    created_nodes = format_node_display(database.get_user_nodes(session.get("sub_id")))
    return render_template(
        "profile.html",
        user=user,
        saved_nodes=saved_nodes,
        created_nodes=created_nodes,
        loggedin=check_signin(),
    )


@app.route("/settings", methods=["GET", "POST"])
@login_required
def view_settings():
    sub_id = session.get("sub_id")
    db_user = database.get_user(sub_id)

    if request.method == "POST":
        print("FORM:", request.form)
        print("FILES:", request.files)
        username = request.form.get("username", "").strip()
        bio = request.form.get("bio", "").strip()

        # in case of empty input, keep whatever was there
        if username == "":
            username = db_user["username"]
        if bio == "":
            bio = db_user.get("bio")

        database.edit_user(sub_id, username, bio, request.files.get("picture"))
        return redirect(url_for("view_profile"))

    user = {
        "name": db_user["username"],
        "bio": db_user.get("bio"),
        "profpicid": db_user.get("profpicid"),
    }
    return render_template("settings.html", user=user, loggedin=check_signin())


@app.route("/notifs")
@login_required
def notifs():
    user_sub_id = session.get("sub_id")
    notifs = database.get_notifs(user_sub_id)

    # format dates
    timestamps = {}
    current_date = ""
    for notif in notifs:
        date = datetime.datetime.fromisoformat(notif["timestamp"])
        date_str = date.strftime("%x")
        if date_str != current_date:
            timestamps[notif["notifid"]] = date_str
            current_date = date_str
        else:
            timestamps[notif["notifid"]] = None

    return render_template("notifications.html", notifs=notifs, dates=timestamps)


@app.route("/delete-notif/<int:notif_id>", methods=('POST',))
@login_required
def delete_notif(notif_id):
    user_sub_id = session.get("sub_id")
    notif = database.get_notif(notif_id)

    if (user_sub_id != notif['recipient']):
        abort(404)
    
    database.delete_notif(notif_id)

    return redirect(url_for("notifs"))


@app.route("/disconnect/<int:node_id1>/<int:node_id2>", methods=('POST',))
@login_required
def disconnect(node_id1,node_id2):
    user_sub_id = session.get("sub_id")
    node1 = database.get_node(node_id1)
    node2 = database.get_node(node_id2)

    if (user_sub_id == node1['subid'] or user_sub_id == node2['subid']):
            database.delete_connection(node_id1, node_id2)

    
    return redirect(url_for("notifs"))


# this threw errors soo
# @app.route("/edit-profile/<int:session.get('sub_id')>")
# @login_required
# def edit_profile():
#     return


# From https://stackoverflow.com/questions/69234307/flask-generate-404-page-if-data-not-found-in-database
@app.errorhandler(404)
def page_404(e):
    return render_template("404.html"), 404
