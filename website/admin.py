from flask import Blueprint, render_template

admin = Blueprint("admin",__name__)

@admin.route("/")
def adminPage():
    return "<h1>admin</h1>"