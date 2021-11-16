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

    return render_template('/librarian/reservations.html',reservations=reservations)

@librarySystem.route('/reservations/delete/<resid>/')
@librarian_required
def delete_res(resid):
    res_info = db_reservation_info(resid)[0]

    db_remove_reservation(resid)
    count_of_book = int(db_actual_count(res_info['title_id'],res_info['library_id'])[0]['count'])
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

    print(f"{until} -- LIB {library_id} -- USER {user_id} -- BOOK {title_id}")
    db_insert_borrow(until,title_id,user_id,session['user']['user_id'],library_id)
    db_remove_reservation(resid)

    return {"err":False,'resToDelete':resid}


@librarySystem.route('/borrowed/')
@librarian_required
def borrowed():
    borrowed = db_borrowed_in_lib(session['user']['library_id'])
    print(*borrowed,sep='\n*******************************************\n')

    return render_template('/librarian/borrowed.html',borrows=borrowed)

@librarySystem.route('/order/')
@librarian_required
def order():
    return render_template('/librarian/order.html')

@librarySystem.route('/books/')
@librarian_required
def booksInLib():
    return render_template('/librarian/booksInLib.html')