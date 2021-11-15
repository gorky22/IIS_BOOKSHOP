from flask import Blueprint, render_template,request

auth = Blueprint("auth",__name__)

@auth.route("/register/")
def authPage():
    return render_template("main/login.html")