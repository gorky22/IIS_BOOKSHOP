from flask import Blueprint, render_template, request,session
from .database import *
import random
import datetime

views = Blueprint("views",__name__)
genres = db_genres()

def format_book_and_authors(book):
    new_book = {
        'title_id':book[0]['title_id'],
        'description':book[0]['description'],
        'title_name':book[0]['title_name'],
        'rating':book[0]['rating'],
        'path_to_picture':book[0]['path_to_picture'],
        'authors':[]
    }

    for book_author in book:
        author = " ".join([book_author['author_name'], book_author['author_surname']])
        new_book['authors'].append(author)
    new_book['authors'] = ", ".join(new_book['authors'])
    new_book['rating_path'] = '/static/img/rating/' + str(round(new_book['rating'])*10)+'percent.png'
    return new_book

def group_by_five(books):
    result = []
    for i in range(0,len(books),5):
        end = i+5 if (i+5) < len(books) else len(books)
        tmp = []
        for book in books[i:end]:
            tmp.append(book)
        result.append(tmp)
    return result

def format_ratings(books):
    for book in books:
        book['rating_path'] = '/static/img/rating/'+str(round(book['rating'])*10)+'percent.png'


@views.route("/")
def viewsPage():
    top = db_top_books()
    
    randomlist = random.sample(range(0, 9), 5)
    books = [top[i] for i in randomlist]
    books = [db_book_info(book['title_id']) for book in books]
    books = [format_book_and_authors(book) for book in books]
    
    return render_template("/main/main.html",books=books,genres=genres)

@views.route("/list/")
def listPage():
    books = db_all_book_info()
    print(books)
    format_ratings(books)
    books = group_by_five(books)

    return render_template("/main/list.html",books=books,genres=genres)
    
@views.route("/detail/")
def detailPage():
    return render_template('/main/detail.html',genres=genres)



@views.route("/libraries/")
def librariesPage():
    libraries = db_libraries()
    return render_template('/main/libraries.html',libraries=libraries,genres=genres)


@views.route("/books/genre/<genreid>")
def booksByGenre(genreid):
    books = db_all_book_with_genre(genreid)
    format_ratings(books)
    books = group_by_five(books)
    genre = db_genre_info(genreid)[0]
    
    return render_template('/main/list.html',books=books,genres=genres,active=genre)
    

@views.route("books/library/<library>")
def booksInLibrary(library):
    books = db_all_book_in_lib(library)
    format_ratings(books)
    books = group_by_five(books)
    library = db_library_info(library)[0]['library_name']

    return render_template("/main/list.html",books=books,library=library,genres=genres,library_name=library)

@views.route("/detail/<bookid>/",methods=["GET","POST"])
def bookDetail(bookid):

    if request.method=="POST":
        if session.get('user'):
            #rezervace
            library_id = request.form.get('lib')
            user_id = session['user']['user_id']
            until = datetime.date.today() + datetime.timedelta(days=10)
            #insert reservace do databaze
            #odecteni 1 ze vztahu mezi knihou a knihovnou

            return {'err':False}
        return {'err':True,'msg':'Rezervace nebyla dokončena, pro dokončení rezervace musíte být přihlášeni.'}


    book = db_book_info(bookid)
    book = format_book_and_authors(book)
    libraries = db_libraries_with_book(book['title_id'])
    
    return render_template('/main/detail.html',book=book,genres=genres,libraries=libraries)


