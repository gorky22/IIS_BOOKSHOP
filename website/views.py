from flask import Blueprint, render_template, request,session


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
    return render_template('/main/detail.html')



@views.route("/form/demo/",methods=["GET","POST"])
def formPage():
    if request.method == "POST":
        print(request.form.get('text'))
    
    return render_template('/main/formTemplate.html')

@views.route("/libraries/")
def librariesPage():
    return render_template('/main/libraries.html')


@views.route("books/library/<library>")
def booksInLibrary(library):
    # get books for library
    return render_template("/main/list.html",library=library)