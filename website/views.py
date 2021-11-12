from flask import Blueprint, render_template

views = Blueprint("views",__name__)

@views.route("/")
def viewsPage():
    return render_template("/main/main.html")

@views.route("/list/")
def listPage():
    book_list = [{'Name' : 'HP1', 'Author': 'J.K.Rowling'},{'Name' : 'HP1', 'Author': 'J.K.Rowling'}]
    return render_template("/main/list.html",book_list=book_list)
    
@views.route("/detail/")
def detailPage():
    return render_template('/main/deatil.html')