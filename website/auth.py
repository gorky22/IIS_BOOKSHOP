from flask import Blueprint, render_template,request
from .database import get_user_with_this_email
auth = Blueprint("auth",__name__)

@auth.route("/register/")
def authPage():

    return render_template("main/login.html")