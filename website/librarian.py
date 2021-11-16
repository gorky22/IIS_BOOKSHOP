from flask import Blueprint, render_template, request,session, wrappers,redirect, url_for
from functools import wraps

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
    return render_template('/librarian/mainLibrary.html')


@librarySystem.route('/reservations/')
@librarian_required
def reservations():
    return render_template('/librarian/reservations.html')

@librarySystem.route('/borrowed/')
@librarian_required
def borrowed():
    return render_template('/librarian/borrowed.html')

@librarySystem.route('/order/')
@librarian_required
def order():
    return render_template('/librarian/order.html')

@librarySystem.route('/order/')
@librarian_required
def booksInLib():
    return render_template('/librarian/booksInLib.html')