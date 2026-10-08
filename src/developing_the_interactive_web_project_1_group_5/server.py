from flask import Flask, render_template, request, url_for, redirect, g, session 
from functools import wraps

import developing_the_interactive_web_project_1_group_5.database as database

app = Flask(__name__)

database.setup()

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('/login')
        return f(*args, **kwargs) #do the normal behavior -- return as it does.
    return decorated

@requires_auth
@app.route("/") 
def landing(): 
    return "<p>It works</p>"

@app.route("/search")
def search():
    return

@app.route("/login")
def login():
    return render_template("login.html")

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