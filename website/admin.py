from flask import Blueprint, render_template

admin = Blueprint("admin",__name__)

@admin.route("/")
def adminPage():
    return render_template("/admin/admin.html")


@admin.route("/libraries/")
def libPage():
    return render_template("admin/libraries.html")


@admin.route("/distributors/")
def distributorsPage():
    return render_template("admin/distributors.html")


@admin.route("/tags/")
def tagsPage():
    return render_template("admin/tags.html")
    