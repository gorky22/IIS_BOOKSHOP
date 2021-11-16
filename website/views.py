from flask import Blueprint, render_template, request,session
from .database import *
import random

views = Blueprint("views",__name__)
genres = db_genres()
@views.route("/")
def viewsPage():
    top = db_top_books()
    
    randomlist = random.sample(range(0, 9), 5)
    books = [top[i] for i in randomlist]
    info = [db_book_info(book['title_id']) for book in books]
    print(*info,sep='\n')
    for book in books:
        book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'

    
    return render_template("/main/main.html",books=books,genres=genres)

@views.route("/list/")
def listPage():
    books = db_books()
    
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)

    return render_template("/main/list.html",books=result,genres=genres)
    
@views.route("/detail/")
def detailPage():
    return render_template('/main/detail.html',genres=genres)



@views.route("/libraries/")
def librariesPage():
    libraries = db_libraries()
    return render_template('/main/libraries.html',libraries=libraries,genres=genres)


@views.route("/books/genre/<genreid>")
def booksByGenre(genreid):
    books = db_books_with_genre(genreid)
    genre = db_genre_info(genreid)[0]
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)
    return render_template('/main/list.html',books=result,genres=genres,active=genre)
    

@views.route("books/library/<library>")
def booksInLibrary(library):
    
    books = db_books_in_lib(library)
    library = db_library_info(library)[0]['library_name']
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
            tmp.append(book)
        result.append(tmp)

    return render_template("/main/list.html",books=result,library=library,genres=genres,library_name=library)

@views.route("/detail/<bookid>")
def bookDetail(bookid):
    book = db_book_by_id(bookid)[0]
    book['rating_path'] = '/static/img/rating/' + str(round(book['rating'])*10)+'percent.png'
    
    print(book)
    return render_template('/main/detail.html',book=book,genres=genres)


#[{'title_name': 'Sila geografie v 21. storočí',
# 'author_name': 'Johannes',
# 'author_surname': 'Straus'},
# {'title_name': 'Sila geografie v 21. storočí',
# 'author_name': 'Terry', 'author_surname': 'Wilson'}]
