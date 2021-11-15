from flask import Blueprint, render_template, request,session
from .database import *

views = Blueprint("views",__name__)

@views.route("/")
def viewsPage():
    return render_template("/main/main.html")

@views.route("/list/")
def listPage():
    book_list = [{'Name' : 'HP1', 'Author': 'J.K.Rowling'},{'Name' : 'HP1', 'Author': 'J.K.Rowling'}]
    print(db_genres())
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
    libraries = db_libraries()
    return render_template('/main/libraries.html',libraries=libraries)


@views.route("books/library/<library>")
def booksInLibrary(library):
    # get books for library

    books = db_books()
    
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)

    return render_template("/main/list.html",books=result,library=library)

@views.route("/detail/<bookid>")
def bookDetail(bookid):
    return render_template('/main/detail.html')



#static/img/libraries/lib7.jpg
#static/img/libraries/lib7.jpg