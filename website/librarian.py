from flask import Blueprint, render_template, request,session, wrappers,redirect, url_for
from functools import wraps
from .database import *
import datetime
import json
from werkzeug.utils import secure_filename
import os

def librarian_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get('user'):
            return redirect(url_for('auth.authPage'))
        if not session['user']['librarian']:
            return redirect(url_for('admin.notPermited'))
        return f(*args,**kwargs)
    return decorated_function




librarySystem = Blueprint('librarySystem',__name__)

@librarySystem.route('/libPage/')
@librarian_required
def homePage():
    library = db_library_info(session['user']['library_id'])[0]
    
    return render_template('/librarian/mainLibrary.html',lib=library['library_name'])


@librarySystem.route('/reservations/')
@librarian_required
def reservations():
    reservations = db_reservations_in_lib(session['user']['library_id'])
    today = datetime.date.today()
    for reserve in reservations:
        reserve['days'] = (reserve['until'] - today).days
        
    return render_template('/librarian/reservations.html',reservations=reservations)

@librarySystem.route('/reservations/delete/<resid>/')
@librarian_required
def delete_res(resid):
    res_info = db_reservation_info(resid)[0]

    db_remove_reservation(resid)
    count_of_book = int(db_actual_count(res_info['library_id'],res_info['title_id'],)[0]['count'])
    count_of_book+=1
    db_update_actual_count(str(count_of_book),res_info['library_id'],res_info['title_id'])

    return {"err":False}

@librarySystem.route('/reservations/confirm/<resid>/',methods=['POST'])
@librarian_required
def confirm_res(resid):
    until = datetime.date.today() + datetime.timedelta(days=31)
    library_id = request.form.get('library_id')
    user_id = request.form.get('user_id')
    title_id = request.form.get('title_id')

    db_insert_borrow(until,title_id,user_id,session['user']['user_id'],library_id)
    db_remove_reservation(resid)

    return {"err":False,'resToDelete':resid}


@librarySystem.route('/borrowed/')
@librarian_required
def borrowed():
    borrowed = db_borrowed_in_lib(session['user']['library_id'])
    today = datetime.date.today()
    for bor in borrowed:
        bor['days'] = (bor['until'] - today).days
    return render_template('/librarian/borrowed.html',borrows=borrowed)

@librarySystem.route('/borrowed/delete/<borid>/')
@librarian_required
def delete_bor(borid):
    borrow_info = db_borrow_info(borid)[0]
    db_remove_borrow(borid)

    count_of_book = int(db_actual_count(borrow_info['library_id'],borrow_info['title_id'])[0]['count'])
    count_of_book+=1
    db_update_actual_count(str(count_of_book),borrow_info['library_id'],borrow_info['title_id'])


    return {"err":False}




@librarySystem.route('/order/')
@librarian_required
def order():
    publishers = db_publishers()
    return render_template('/librarian/order.html',publishers=publishers)

@librarySystem.route('/books/',methods=["POST"])
@librarian_required
def booksInLib():
    if request.method == 'POST':
        books = {}
        for i in request.form:
            books = json.loads(i)
        
        id_of_order = add_order(session['user']['user_id'],books['publisher'])
        ids = books['id_list']
        counts = books['order']
        add_books_to_order(id_of_order,ids,counts)
        return {'err':False}


@librarySystem.route('/publisher/books/<pubid>/')
@librarian_required
def booksByPublisher(pubid):
    books = db_book_by_publisher(pubid)
    
    return {'err': None,'books':books}

@librarySystem.route('/booklis/')
@librarian_required
def booksByLib():
    books = db_all_book_in_lib(session['user']['library_id'])
    for book in books:
        author = db_book_authors(book['title_id'])[0]
        book['author'] = author['author_name'] + " " + author['author_surname']
        book['count'] = db_actual_count(session['user']['library_id'],book['title_id'])[0]['count']
    return render_template('/librarian/booksInLib.html',books=books)

@librarySystem.route('/bookdelete/<bookid>/',methods=['GET'])
@librarian_required
def deleteBook(bookid):
    db_delete_book(bookid)
    return {'err':False}

@librarySystem.route('/addbooks/',methods=['GET','POST'])
@librarian_required
def addBook():
    
    
    if request.method == "POST":
        author_ids = []
        UPLOAD_FOLDER = "website/static/img"
        STATIC_FOLDER = "/static/img"
        if 'names[]' in request.form:
            new_surnames = request.form.getlist("surnames[]")[0].split(",")
            new_names = request.form.getlist("names[]")[0].split(",")
            for i in range(len(new_surnames)):
                id_of_new = db_add_author(new_names[i],new_surnames[i])
                author_ids.append(id_of_new)
            
        if 'author_ids[]' in request.form:
            authors = request.form.getlist("author_ids[]")[0].split(",")
            for id_auth in authors:
                author_ids.append(int(id_auth))

        file = request.files.getlist("file")[0]
        filename = secure_filename(file.filename)
        
        path_to_new_file = os.path.join(UPLOAD_FOLDER,filename)
        path_to_picture = os.path.join(STATIC_FOLDER,filename)
        file.save(path_to_new_file)

        form_title_name = request.form.get('title_name')
        form_title_date = request.form.get('date')
        form_title_isbn = request.form.get('isbn')
        form_title_desc = request.form.get('description')
        rating = 0
        publisher_id = request.form.get('publisher_id')
        id_of_inserted_book = db_insert_book(form_title_date,form_title_isbn,rating,form_title_desc,path_to_picture,form_title_name,publisher_id)
        




        for id_author in author_ids:
            db_add_book_author(id_of_inserted_book,id_author)
            
        
        return {'err':False,'url':url_for('librarySystem.booksByLib')}

    authors = db_authors()
    publishers = db_publishers()
    return render_template('/librarian/books.html',authors=authors,publishers=publishers)


