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
    

@distribSystem.route('/books/')
@distrib_required
def distribBooks():
    
    return render_template('distributor/books.html')




