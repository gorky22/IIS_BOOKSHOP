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
#@admin_required
def adminPage():
    if request.method == "POST":
        if "nm" in request.form:
            users = find_user(request.form["nm"])
            
    else:
        users = get_all_users()
        libs = db_libraries()

    return render_template("/admin/admin.html", users=users, libraries=libs)


@admin.route("delete/", methods=["POST"])
#@admin_required
def userDelete():
    
    if request.method == "POST" :
        email = request.form.get("email")  
        print("Vymazal som uzivatela", email)
        delete_user(email)

        return {'message' : "ok"}


@admin.route("deleteLib/", methods=["POST"])
#@admin_required
def libDelete():
    
    if request.method == "POST" :
        email = request.form.get("email")  
        print("Vymazal som knihovnu", email)
        delete_library(email)

        return {'message' : "ok"}


@admin.route("deleteTag/", methods=["POST"])
#@admin_required
def tagDelete():
    
    if request.method == "POST" :
       
        genre_id = request.form.get("genre_id")  
        print("Vymazal som Tag", genre_id)
        delete_tag(genre_id)

        return {'message' : "ok"}


@admin.route("/user/<useremail>")
#@admin_required
def get_user_by_id(useremail):
    user = get_user_with_this_email(useremail)
    #print(user[0])
    return {'user' : user[0]}


@admin.route("/library/<email>")
#@admin_required
def get_lib_by_email(email):
    library = find_library(email)
    
    #print(library[0])
    return {'lib' : library[0]}


@admin.route("/tags/<id>")
#@admin_required
def get_tag_by_id(id):
    #tag = find_library(id)
    
    tag = [{'name' : 'fero'}]

    #print(library[0])
    return {'tag' : tag[0]}

@admin.route('/editUser/', methods=["POST"])
#@admin_required
def edit_user():
    #print("EDITOVANIE USERA")
    if request.method == "POST" :
        data = request.form  
        #print("Data", data)

        # knihovnikovi nebola pridana kniznica
        if data['librarian'] == '1' and data['library_id'] == '0':
            return {'message' : 'err'}
        else:
            update_user_db(data)
            return {'message' : 'ok'}


@admin.route('/editTag/', methods=["POST"])
#@admin_required
def edit_tag():
    #print("EDITOVANIE USERA")
    if request.method == "POST" :
        data = request.form  
        print(data)

        update_tag_db(data)
        
        return {'message' : 'ok'}



@admin.route('/editLib/', methods=["POST"])
#@admin_required
def edit_lib():
    if request.method == "POST" :
        data = request.form  
        print("Data", data)
        update_lib_db(data)

        return {'message' : 'ok'}


@admin.route('/addLib/', methods=["POST"])
#@admin_required
def add_lib():
    if request.method == "POST" :
        data = request.form  
        print(data)
        
        insert_into_lib(data)

        return {'message' : 'ok'}


@admin.route('/addTag/', methods=["POST"])
#@admin_required
def add_tag():
    if request.method == "POST" :
        data = request.form  
        print(data)
        ##insert_into_lib(data)

        return {'message' : 'ok'}


@admin.route("/libraries/", methods=["POST", "GET"])
#@admin_required
def libPage():
    if request.method == "POST":
        if "nm" in request.form:
            libraries = find_library(request.form["nm"])
            
    else:
        libraries = db_libraries()
        
    print(*libraries, sep='\n')
    return render_template("admin/libraries.html", libraries=libraries)


@admin.route("/distributors/", methods=["POST", "GET"])
#@admin_required
def distributorsPage():
    if request.method == "POST":
        if "nm" in request.form:
            distributors = find_distributors(request.form["nm"])
            
    else:
        distributors = db_distributors()
        
    return render_template("admin/distributors.html", distributors=distributors)

@admin.route("/distributors/delete/", methods=["POST"])
#@admin_required
def distributorDelete():
    
    if request.method == "POST" :
        email = request.form.get("email")  
        delete_distributors(email)

        return {'message' : "ok"}

@admin.route("/distributors/<distributoremail>", methods=["GET"])
#@admin_required
def get_distributors_by_email(distributoremail):
    distributor = find_distributors(distributoremail)
    #distributor = [{"publisher_name":"cc","adress":"ss","publisher_email":"ss","town":"sss"}]
    print(distributor[0])
    return {'dist' : distributor[0]}

@admin.route('/editDist/', methods=["POST"])
#@admin_required
def edit_dist():
    if request.method == "POST" :
        data = request.form  
        
        update_distributor_db(data)

        return {'message' : 'ok'}

@admin.route('/addDist/', methods=["POST"])
#@admin_required
def add_dist():
    if request.method == "POST" :
        data = request.form  
        insert_into_dist(data)

        return {'message' : 'ok'}

@admin.route("/tags/", methods=["POST", "GET"])
#@admin_required
def tagsPage():
    if request.method == "POST":
        if "nm" in request.form:
            tags = db_tags(tag=request.form["nm"])
            
    else:
        tags = db_tags()
    return render_template("admin/tags.html", tags=tags)
    

@admin.route('/notPermited/')
def notPermited():
    return render_template('admin/notPermited.html')