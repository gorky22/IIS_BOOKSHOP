from flask import Blueprint, render_template

views = Blueprint("views",__name__)

@views.route("/")
def viewsPage():
    return render_template("/main/main.html")