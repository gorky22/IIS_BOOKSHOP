from flask import Blueprint, render_template, request

from .database import *

admin = Blueprint("admin",__name__)

@admin.route("/", methods=["POST", "GET"])
def adminPage():
    if request.method == "POST":
        if "nm" in request.form:
            users = find_user(request.form["nm"])
            #users = [{'email' : 'najdeny@email', 'name' : request.form["nm"], 'data' : '21.12.1988'}]
            
    else:
        users = get_all_users()
        print(users[0])
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

        return {'message' : f'Vymazal si uzivatela {email}'}
        
@admin.route("/user/<useremail>")
def get_user_by_id(useremail):
    user = get_user_with_this_email(useremail)
    print
    return {'user' : user[0]}



@admin.route("/libraries/")
def libPage():
    return render_template("admin/libraries.html")


@admin.route("/distributors/")
def distributorsPage():
    return render_template("admin/distributors.html")


@admin.route("/tags/")
def tagsPage():
    return render_template("admin/tags.html")
    