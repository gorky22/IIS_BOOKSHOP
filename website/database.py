from flask import Blueprint, render_template

database = Blueprint("database",__name__)

@database.route("/")
def databasePage():
    return "<h1>database</h1>"