from flask import Blueprint, render_template

auth = Blueprint("auth",__name__)

@auth.route("/")
def authPage():
    return "<h1>auth</h1>"