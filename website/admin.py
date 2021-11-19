from flask import Blueprint, render_template, request,session,redirect,url_for
from functools import wraps
from .database import *
from werkzeug.utils import secure_filename
import os

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


####    USER    #### 
####################
@admin.route("/", methods=["POST", "GET"])
#@admin_required
def adminPage():
    if request.method == "POST":
        if "nm" in request.form:
            users = find_user(request.form["nm"])
    else:
        users = get_all_users()
        libs = db_libraries()
        dis = db_distributors()

    return render_template("/admin/admin.html", users=users, libraries=libs, distributors=dis)


# Delete user
@admin.route("delete/", methods=["POST"])
#@admin_required
def userDelete():
    if request.method == "POST" :
        email = request.form.get("email")  
        print("Vymazal som uzivatela", email)
        delete_user(email)

        return {'message' : "ok"}


# Get info from user
@admin.route("/user/<useremail>")
#@admin_required
def get_user_by_id(useremail):
    user = get_user_with_this_email(useremail)
    dis = distributor_alma_mater(useremail)
    
    if len(dis) == 0 :
        return {'user' : user[0],
            'dis' : ""}    
    else :
        return {'user' : user[0],
            'dis' : dis[0]}


# Edit user
@admin.route('/editUser/', methods=["POST"])
#@admin_required
def edit_user():
    #print("EDITOVANIE USERA")
    if request.method == "POST" :
        data = request.form  

        # knihovnikovi nebola pridana kniznica
        if data['librarian'] == '1' and data['library_id'] == '0':
            return {'message' : 'err'}
        else:
            update_user_db(data)
            
            return {'message' : 'ok'}


####    LIBRARY    #### 
#######################
@admin.route("/libraries/", methods=["POST", "GET"])
#@admin_required
def libPage():
    if request.method == "POST":
        if "nm" in request.form:
            libraries = find_library(request.form["nm"])
    else:
        libraries = db_libraries()
        
    return render_template("admin/libraries.html", libraries=libraries)


# Delete Library
@admin.route("deleteLib/", methods=["POST"])
#@admin_required
def libDelete():
    if request.method == "POST" :
        email = request.form.get("email")  
        delete_library(email)

        return {'message' : "ok"}


# Get info from library
@admin.route("/library/<email>")
#@admin_required
def get_lib_by_email(email):
    library = find_library(email)
    dis = distributor_alma_mater(email)
    
    return {'lib' : library[0]}


# Edit library
@admin.route('/editLib/', methods=["POST"])
#@admin_required
def edit_lib():
    UPLOAD_FOLDER = "website/static/img"
    STATIC_FOLDER = "/static/img"
    if request.method == "POST" :
        name = request.form.get('library_name')
        opening_hours = request.form.get('opening_hours')
        web_link = request.form.get('webpage_link')
        lib_email = request.form.get('library_email')
        old_email = request.form.get('old_email')

        file = request.files.getlist("file")[0]
        filename = secure_filename(file.filename)
        
        path_to_new_file = os.path.join(UPLOAD_FOLDER,filename)
        path_to_picture = os.path.join(STATIC_FOLDER,filename)
        file.save(path_to_new_file) 

        data = {
        "old_email" : old_email,
        "library_name" : name,
        "opening_hours" : opening_hours,
        "webpage_link" : web_link,
        "path_to_picture" : path_to_picture,
        "library_email" : lib_email,
        }
        print("Data", data)
        update_lib_db(data)

        return {'message' : 'ok'}


# Add Library
@admin.route('/addLib/', methods=["POST"])
#@admin_required
def add_lib():
    UPLOAD_FOLDER = "website/static/img"
    STATIC_FOLDER = "/static/img"
    if request.method == "POST" :
        name = request.form.get('library_name')
        town = request.form.get('town')
        description = request.form.get('description')
        address = request.form.get('adress')
        opening_hours = request.form.get('opening_hours')
        web_link = request.form.get('webpage_link')
        lib_email = request.form.get('library_email')

        file = request.files.getlist("file")[0]
        filename = secure_filename(file.filename)
        
        path_to_new_file = os.path.join(UPLOAD_FOLDER,filename)
        path_to_picture = os.path.join(STATIC_FOLDER,filename)
        file.save(path_to_new_file)

        data = {
        "library_name" : name,
        "town" : town,
        "adress" : address,
        "description" : description,
        "opening_hours" : opening_hours,
        "webpage_link" : web_link,
        "path_to_picture" : path_to_picture,
        "library_email" : lib_email,
        }

        print(data)
        res = insert_into_lib(data)
        if res == True:
            return {'message' : 'ok'}
        else:
            return {'message' : 'err'}



####    TAG    #### 
###################
@admin.route("/tags/", methods=["POST", "GET"])
#@admin_required
def tagsPage():
    if request.method == "POST":
        if "nm" in request.form:
            tags = db_tags(tag=request.form["nm"])
    else:
        tags = db_tags()
    return render_template("admin/tags.html", tags=tags)


# Delete Tag
@admin.route("deleteTag/", methods=["POST"])
#@admin_required
def tagDelete():
    if request.method == "POST" :
        genre_id = request.form.get("genre_id")  
        delete_tag(genre_id)

        return {'message' : "ok"}


# Get info from Tag
@admin.route("/tags/<id>")
#@admin_required
def get_tag_by_id(id):
    tag = db_tags(id)
    return {'tag' : tag[0]}


# Edit Tag
@admin.route('/editTag/', methods=["POST"])
#@admin_required
def edit_tag():
    #print("EDITOVANIE USERA")
    if request.method == "POST" :
        data = request.form  
        update_tag_db(data)
        
        return {'message' : 'ok'}


# Add tag
@admin.route('/addTag/', methods=["POST"])
#@admin_required
def add_tag():
    if request.method == "POST" :
        data = request.form  
        res = insert_tag(data)

        if res == True :
            return {'message' : 'ok'}
        else:
            return {'message' : 'err'}


####    DISTRIBUTORS    #### 
############################
@admin.route("/distributors/", methods=["POST", "GET"])
#@admin_required
def distributorsPage():
    if request.method == "POST":
        if "nm" in request.form:
            distributors = find_distributors(request.form["nm"])
            
    else:
        distributors = db_distributors()
        
    return render_template("admin/distributors.html", distributors=distributors)


# Delete Distributor
@admin.route("/distributors/delete/", methods=["POST"])
#@admin_required
def distributorDelete():
    if request.method == "POST" :
        email = request.form.get("email")  
        delete_distributors(email)

        return {'message' : "ok"}


# Get info from Distributor
@admin.route("/distributors/<distributoremail>", methods=["GET"])
#@admin_required
def get_distributors_by_email(distributoremail):
    distributor = find_distributors(distributoremail)

    return {'dist' : distributor[0]}


# Edit distributor
@admin.route('/editDist/', methods=["POST"])
#@admin_required
def edit_dist():
    if request.method == "POST" :
        data = request.form  
        
        update_distributor_db(data)

        return {'message' : 'ok'}


# Add Distributor
@admin.route('/addDist/', methods=["POST"])
#@admin_required
def add_dist():
    if request.method == "POST" :
        data = request.form  
        insert_into_dist(data)

        return {'message' : 'ok'}


    
@admin.route('/notPermited/')
def notPermited():
    return render_template('admin/notPermited.html')