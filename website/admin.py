from flask import Blueprint, render_template, request

from website.database import delete_user, find_user, get_all_users, get_user_with_this_email

admin = Blueprint("admin",__name__)

@admin.route("/", methods=["POST", "GET"])
def adminPage():
    if request.method == "POST":
        if "nm" in request.form:
            users = find_user(request.form["nm"])
            #users = [{'email' : 'najdeny@email', 'name' : request.form["nm"], 'data' : '21.12.1988'}]
            
    else:
        users = get_all_users()
        #users = [{'e-mail' : 'gorky@srac.sk', 'name' : 'Pan gorky', 'data' : '21.12.1988'},
        #         {'e-mail' : 'Hanzik@beast.sk', 'name' : 'Janicko', 'data' : '11.10.1982'},
        #         {'e-mail' : 'Tomik@mergesort.sk', 'name' : 'Shelby z brna', 'data' : '1.1.2002'}]

    return render_template("/admin/admin.html", users=users)


@admin.route("delete/", methods=["POST"])
def userDelete():
    
    if request.method == "POST" :
        email = request.form.get("email")  
        delete_user(email)

        return {'message' : f'Vymazal si uzivatela {email}'}
        

@admin.route("/libraries/")
def libPage():
    return render_template("admin/libraries.html")


@admin.route("/distributors/")
def distributorsPage():
    return render_template("admin/distributors.html")


@admin.route("/tags/")
def tagsPage():
    return render_template("admin/tags.html")
    