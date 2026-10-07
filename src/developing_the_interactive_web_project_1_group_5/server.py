from flask import Flask, render_template, request, url_for, redirect

import developing_the_interactive_web_project_1_group_5.database as database

app = Flask(__name__)

database.setup()


@app.route("/") 
def landing(): 
    return "<p>It works</p>"

@app.route("/search")
def search():
    return

@app.route("/login")
def login():
    return

@app.route("/sign-up")
def sign_up():
    return

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