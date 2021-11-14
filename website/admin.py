from flask import Blueprint, render_template, request

admin = Blueprint("admin",__name__)

@admin.route("/", methods=["POST", "GET"])
def adminPage():
    #users = [{'e-mail' : 'gorky@srac.sk', 'name' : 'Pan gorky', 'data' : '21.12.1988'}]


    if request.method == "POST":
        if "nm" in request.form:
            users = [{'e-mail' : 'najdeny@email', 'name' : request.form["nm"], 'data' : '21.12.1988'}]
        else:
            users = [{'e-mail' : 'gorky@srac.sk', 'name' : 'Pan gorky', 'data' : '21.12.1988'},
                    {'e-mail' : 'Hanzik@beast.sk', 'name' : 'Janicko', 'data' : '11.10.1982'},
                    {'e-mail' : 'Tomik@mergesort.sk', 'name' : 'Shelby z brna', 'data' : '1.1.2002'}]
    else:
        users = [{'e-mail' : 'gorky@srac.sk', 'name' : 'Pan gorky', 'data' : '21.12.1988'}]

    return render_template("/admin/admin.html", users=users)


@admin.route("/admin/delete/", methods=["POST"])
def userDelete():
    fero = {"name": "sprava prijata"}
    
    if request.method == "POST" :
    
        fero = {"name": "sprava prijata"}
        return fero
    return fero

@admin.route("/libraries/")
def libPage():
    return render_template("admin/libraries.html")


@admin.route("/distributors/")
def distributorsPage():
    return render_template("admin/distributors.html")


@admin.route("/tags/")
def tagsPage():
    return render_template("admin/tags.html")
    