from flask import Blueprint, render_template, request,session, wrappers,redirect, url_for
from functools import wraps
from .database import *
import datetime

def librarian_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get('user'):
            return redirect(url_for('auth.authPage'))
        if not session['user']['librarian']:
            return redirect(url_for('admin.loginPage'))
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
    for res in reservations:
        res['book_name'] = db_book_by_id(res['title_id'])[0]['title_name']
    print(reservations)
    return render_template('/librarian/reservations.html',reservations=reservations)

@librarySystem.route('/reservations/delete/<resid>/')
@librarian_required
def delete_res(resid):
    db_remove_reservation(resid)
    return {"err":False}

@librarySystem.route('/reservations/confirm/<resid>/',methods=['POST'])
@librarian_required
def confirm_res(resid):
    # take form arguments
    # take res arguments
    # delete res
    # add to borrowed
    until = datetime.date.today() + datetime.timedelta(days=31)
    library_id = request.form.get('library_id')
    user_id = request.form.get('user_id')
    title_id = request.form.get('title_id')

    print(f"{until} -- LIB {library_id} -- USER {user_id} -- BOOK {title_id}")
    db_insert_borrow(until,title_id,user_id,session['user']['user_id'],library_id)
    db_remove_reservation(resid)

    return {"err":False,'resToDelete':resid}


@librarySystem.route('/borrowed/')
@librarian_required
def borrowed():
    
    return render_template('/librarian/borrowed.html')

@librarySystem.route('/order/')
@librarian_required
def order():
    return render_template('/librarian/order.html')

@librarySystem.route('/books/')
@librarian_required
def booksInLib():
    return render_template('/librarian/booksInLib.html')