from os import sep
from flask import Blueprint, render_template, request,session,redirect,url_for
from .database import *
import random
import datetime
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get('user'):
            return redirect(url_for('auth.authPage'))
        if not session['user']['reader'] and not session['user']['admin']:
            return redirect(url_for('admin.notPermited'))
        return f(*args,**kwargs)
    return decorated_function

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
    format_ratings(books)
    books = group_by_five(books)

    return render_template("/main/list.html",books=books,genres=genres)
    
@views.route("/detail/")
def detailPage():
    return render_template('/main/detail.html',genres=genres)



@views.route("/libraries/")
def librariesPage():
    libraries = db_libraries()
    for lib in libraries:
        counts = db_counts_of_books_in_library(lib['library_id'])
        if len(counts) > 0:
            lib['count'] = sum(count['count'] for count in counts)
        else:
            lib['count'] = 0
    return render_template('/main/libraries.html',libraries=libraries,genres=genres)


@views.route("/books/genre/<genreid>/")
def booksByGenre(genreid):
    books = db_all_book_with_genre(genreid)
    format_ratings(books)
    books = group_by_five(books)
    genre = db_genre_info(genreid)[0]
    
    return render_template('/main/list.html',books=books,genres=genres,active=genre)
    

@views.route("books/library/<library>/")
def booksInLibrary(library):
    session['lib'] = int(library)
    

    books = db_all_book_in_lib(library)
    format_ratings(books)
    books = group_by_five(books)
    library = db_library_info(library)[0]['library_name']
    
    return render_template("/main/list.html",books=books,library=library,genres=genres,library_name=library)

@views.route("/isbookAvailible/<bookid>/<libid>/",methods=["GET","POST"])
def is_book_availible(bookid,libid):
    count_of_book = int(db_actual_count(libid,bookid)[0]['count'])
    if count_of_book > 0:
        return {'answer':True}
    return {'answer':False}

@views.route('/addToQue/',methods=['POST'])
def addToQue():
    user_id = session['user']['user_id']
    lib_id = request.form.get('lib')
    book_id = request.form.get('book')
    add_to_queue(book_id,lib_id,user_id)
    return {'err':False}

@views.route("/detail/<bookid>/",methods=["GET","POST"])
def bookDetail(bookid):
    similar_books=find_similar_genre_book(bookid)
    for i in range(len(similar_books)):
        if similar_books[i]['title_id'] == int(bookid):
            del similar_books[i]
            break
    format_ratings(similar_books)
    

    if request.method=="POST":
        if session.get('user'):
            #rezervace
            if session['user'].get('reader'):
                library_id = request.form.get('lib')
                user_id = session['user']['user_id']
                until = datetime.date.today() + datetime.timedelta(days=10)
                
                if len(db_res_with_book_lib_user(bookid,user_id,library_id)) == 0 and len(db_bor_with_book_lib_user(bookid,user_id,library_id)) == 0:
                    count_of_book = int(db_actual_count(library_id,bookid)[0]['count'])
                    if count_of_book > 0:
                        db_insert_reservation(until,bookid,user_id,library_id)
                        count_of_book-=1
                        db_update_actual_count(str(count_of_book),library_id,bookid)
                        count_of_book = int(db_actual_count(library_id,bookid)[0]['count'])
                        return {'err':False}
                    return {'err': True, 'msg':'Tato kniha již není k dispozici v této knihovně'}
                return {'err':True,'msg':'Na tuto knížku již učiněnou rezervaci nebo výpůjčku máte'}
            return {'err':True,'msg':'Nemůžete rezervovat knihy, nemáte práva čtenáře.'}
        return {'err':True,'msg':'Rezervace nebyla dokončena, pro dokončení rezervace musíte být přihlášeni.'}


    book = db_book_info(bookid)
    book = format_book_and_authors(book)
    libraries = db_libraries_with_book(book['title_id'])


    
    return render_template('/main/detail.html',book=book,genres=genres,libraries=libraries,similar=similar_books)

@views.route('/rate/book/',methods=['POST'])
def rateBook():
    book_id = request.form.get('title_id')
    old_rating = float(request.form.get('old_value'))
    new_rating = float(request.form.get('value'))
    if session['user']:
        if session['user']['reader']:
            result = (old_rating+new_rating)/2
            result = float("%.1f" % result)
            db_update_rating(book_id,result)
            path_to_image = '/static/img/rating/' + str(round(result)*10)+'percent.png'
            return {'err':False,'new_value':result,'path_to_image':path_to_image}
        return {'err':True,'msg':'Pro hodnocení musíte mít práva čtenáře.'}
    return {'err':True,'msg':'Pro hodnocení knih se musíte přihlássit'}

@views.route("/user/reservations/")
@login_required
def userReservation():
    reservations = db_reserved_books(session['user']['user_id'])
    return render_template('/main/userReservation.html',reservations=reservations,genres=genres)


@views.route("/reservation/delay/<resid>/")
def delayReservation(resid):
    reservation = db_reservation_info(resid)[0]
    reservation["until"] = reservation["until"] + datetime.timedelta(days=10)
    db_update_reservation_time(resid,reservation['until'])
    return {'err':False,'newtime':reservation['until'].strftime("%d. %m. %Y")}


@views.route("/user/borrowed/")
@login_required
def borrowedReservation():
    borrowed = db_borrowed_books(session['user']['user_id'])
    return render_template('/main/userBorrows.html',borrowed=borrowed,genres=genres)

@views.route("/borrow/delay/<borid>/")
def delayBorrow(borid):
    borrow = db_borrow_info(borid)[0]
    borrow["until"] = borrow["until"] + datetime.timedelta(days=10)
    db_update_borrow_time(borid,borrow['until'])
    return {'err':False,'newtime':borrow['until'].strftime("%d. %m. %Y")}

@views.route("/surveys/")
@login_required
def surveysPage():
    libraries = db_libraries()

    return render_template('/main/surveys.html',libs=libraries,genres=genres)


@views.route("/surveys/<libid>/",methods=['GET','POST'])
@login_required
def surveysDetail(libid):
    if request.method == 'POST':
        if session['user']['reader']:
            title_id = request.form.get('title_id')
            lib_id = request.form.get('lib_id')
            user_id = session['user']['user_id']
            db_insert_new_vote(title_id,lib_id,user_id)
            return {'err':False}
        return {'err':True,'msg':'Na tuto operaci nemáte práva'}
    
    
    books = db_all_books_not_in_lib(libid)
    library = db_library_info(libid)[0]
    return render_template('/main/surveyDetail.html',books=books,library=library,genres=genres)