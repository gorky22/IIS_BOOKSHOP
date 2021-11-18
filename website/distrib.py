from flask import Blueprint, render_template, request,session, wrappers,redirect, url_for
from functools import wraps
from .database import *
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
        ALLOWED_FILES = ['.png','.jpg','.jpeg','.webp','.svg']
        author_ids = []
        if 'names[]' in request.form:
            new_surnames = request.form.getlist("surnames[]")[0].split(",")
            new_names = request.form.getlist("names[]")[0].split(",")
            # !!!ADD AUTHORS TO DATABASE AND GET THEIR IDS!!!!!!!
        if 'author_ids[]' in request.form:
            author_ids = request.form.getlist("author_ids[]")[0].split(",")
            # !!! ADD IDS TO BOOK_TITLE_AUHTOR
            print(author_ids)
        
        return {'err':False}

    authors = db_authors()
    return render_template('distributor/books.html',authors=authors)


# release data
# ISBN
# rating = 0
# description
# path_to_picture -> input file
# title_name
# publisher_id -> default to session['user']['publisher_id']

