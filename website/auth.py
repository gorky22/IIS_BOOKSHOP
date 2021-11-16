import datetime
from flask import Blueprint, render_template,request,session,redirect,url_for
from .database import get_user_with_this_email, add_user
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

auth = Blueprint("auth",__name__)

@auth.route("/register/",methods=["POST","GET"])
def authPage():
    if request.method == "POST":
        
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        surName = request.form.get('surName')
        password = sha256.encrypt(request.form.get('pass1'))
        birth_date = datetime.date(int(request.form.get('year')),
                                   int(request.form.get('month')),
                                   int(request.form.get('day')))

        if len(get_user_with_this_email(email)) > 0:
            return {'message': 'Uživatel s tímto e-mailem již existuje.','err': True}
        else:
            add_user(firstName,surName,email,birth_date,password,reader=True)
            user_from_db = get_user_with_this_email(email)[0]
            session['logged_in'] = True
            del user_from_db['Password']
            session['user'] = user_from_db
            return {'message': 'OK','err': False,'url': url_for('views.viewsPage')}
        


    return render_template("main/register.html")

@auth.route("/login/",methods=["POST","GET"])
def loginPage():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('pass')
        user_from_db = get_user_with_this_email(email)
        if len(user_from_db) > 0:
            user_from_db = user_from_db[0]
            if sha256.verify(password,user_from_db.get('Password')):
                session['logged_in'] = True
                del user_from_db['Password']
                session['user'] = user_from_db
                #print(session['user'])
                return {'message' : 'OK','err':False,'url': url_for('views.viewsPage')}
            return {'message' : 'Spatne heslo','err':True}
        else:
            return {'message' : 'E-mail neexistuje','err':True}

    return render_template("main/login.html")

@auth.route('/logOut/')
def logout():
    session.clear()
    return redirect(url_for('views.viewsPage'))


