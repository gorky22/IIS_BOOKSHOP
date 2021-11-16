from flask import Blueprint, render_template, request,session,redirect,url_for
from functools import wraps
from .database import *

def admin_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get('user'):
            return redirect(url_for('auth.loginPage'))
        if not session['user']['admin']:
            return redirect(url_for('admin.notPermited'))
        return f(*args,**kwargs)
    return decorated_function


admin = Blueprint("admin",__name__)

@admin.route("/", methods=["POST", "GET"])
def adminPage():
    if request.method == "POST":
        if "nm" in request.form:
            users = find_user(request.form["nm"])
            #users = [{'email' : 'najdeny@email', 'name' : request.form["nm"], 'data' : '21.12.1988'}]
            
    else:
        users = get_all_users()
        #print(users)
        #users = [{'e-mail' : 'gorky@srac.sk', 'name' : 'Pan gorky', 'data' : '21.12.1988'},
        #         {'e-mail' : 'Hanzik@beast.sk', 'name' : 'Janicko', 'data' : '11.10.1982'},
        #         {'e-mail' : 'Tomik@mergesort.sk', 'name' : 'Shelby z brna', 'data' : '1.1.2002'}]

    return render_template("/admin/admin.html", users=users)


@admin.route("delete/", methods=["POST"])
def userDelete():
    
    if request.method == "POST" :
        email = request.form.get("email")  
        print("Vymazal som uzivatela", email)
        #delete_user(email)

        return {'message' : "ok"}
        
@admin.route("/user/<useremail>")
def get_user_by_id(useremail):
    user = get_user_with_this_email(useremail)
    print
    return {'user' : user[0]}

@admin.route('/editUser/', methods=["POST"])
def edit_user():
    print("EDITOVANIE USERA")
    if request.method == "POST" :
        data = request.form  
        print("Data", data)
        #update_user_db(data)

        return {'message' : 'ok'}

@admin.route("/libraries/")
def libPage():
    return render_template("admin/libraries.html")


@admin.route("/distributors/")
def distributorsPage():
    return render_template("admin/distributors.html")


@admin.route("/tags/")
def tagsPage():
    return render_template("admin/tags.html")
    

@admin.route('/notPermited/')
def notPermited():
    return render_template('admin/notPermited.html')