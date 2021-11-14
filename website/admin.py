from flask import Blueprint, render_template

admin = Blueprint("admin",__name__)

@admin.route("/")
def adminPage():
    users = [{'e-mail' : 'gorky@srac.sk', 'name' : 'Pan gorky', 'data' : '21.12.1988'},
             {'e-mail' : 'Hanzik@beast.sk', 'name' : 'Janicko', 'data' : '11.10.1982'},
             {'e-mail' : 'Tomik@merge.sk', 'name' : 'Shelby z brna', 'data' : '1.1.2002'}]
    return render_template("/admin/admin.html", users=users)


@admin.route("/libraries/")
def libPage():
    return render_template("admin/libraries.html")


@admin.route("/distributors/")
def distributorsPage():
    return render_template("admin/distributors.html")


@admin.route("/tags/")
def tagsPage():
    return render_template("admin/tags.html")
    