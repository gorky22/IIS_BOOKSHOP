from flask import Blueprint, render_template, request,session, wrappers,redirect, url_for
from functools import wraps
from .database import *
from werkzeug.utils import secure_filename
import os
import datetime

def distrib_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get('user'):
            return redirect(url_for('auth.authPage'))
        if not session['user']['distributor']:
            return redirect(url_for('admin.notPermited'))
        return f(*args,**kwargs)
    return decorated_function




distribSystem = Blueprint('distribSystem',__name__)

@distribSystem.route('/')
@distrib_required
def distribHome():
    distributor = db_distributor_info(session['user']['publisher_id'])[0]
    return render_template('distributor/home.html',publisher=distributor)

@distribSystem.route('/orders/')
@distrib_required
def distribOrders():
    orders = db_unfinished_orders_for_distributor(session['user']['publisher_id'])
    books_in_order = [db_info_about_books_in_order(order['order_id']) for order in orders]
    for i in range(len(orders)):
        orders[i]['books'] = books_in_order[i]
    return render_template('distributor/orders.html',orders=orders)

@distribSystem.route('/order/confirm/<orderid>/')
@distrib_required
def confirmOrder(orderid):
    books = db_info_about_books_in_order(orderid)
    order = db_order_info(orderid)[0]
    librarian = db_user_info(order['librarian_id'])[0]
    for book in books:
        actual_count = db_actual_count(librarian['library_id'],book['title_id'])
        if len(actual_count) == 0:
            db_insert_new_count(book['title_id'],librarian['library_id'],book['count'])
        else:
            new_count = int(actual_count[0]['count']) + int(book['count'])
            db_update_actual_count(new_count,librarian['library_id'],book['title_id'])
    db_make_order_done(orderid)

    return {'err':False,'order':orderid}

@distribSystem.route('/books/',methods=['GET','POST'])
@distrib_required
def distribBooks():
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
        publisher_id = session['user']['publisher_id']
        
        id_of_inserted_book = db_insert_book(form_title_date,form_title_isbn,rating,form_title_desc,path_to_picture,form_title_name,publisher_id)
        for id_author in author_ids:
            db_add_book_author(id_of_inserted_book,id_author)
            
        
        return {'err':False,'url':url_for('distribSystem.distribBooks')}

    authors = db_authors()
    return render_template('distributor/books.html',authors=authors)

@distribSystem.route('/booklist/',methods=['GET','POST'])
@distrib_required
def distribListBooks():
    

    books = db_books_with_publisher(session['user']['publisher_id'])
    for book in books:
        author = db_book_authors(book['title_id'])[0]
        book['author'] = author['author_name'] + " " + author['author_surname']
    
    return render_template('distributor/bookList.html',books=books)

@distribSystem.route('/bookdelete/<bookid>/',methods=['GET'])
@distrib_required
def deleteBook(bookid):
    db_delete_book(bookid)
    return {'err':False}



