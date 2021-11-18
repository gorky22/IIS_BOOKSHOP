from flask import Flask
import mysql.connector as mysql

HOST = "eu-cdbr-west-01.cleardb.com" 
DATABASE = "heroku_c8164a0212f5cf6"
USER = "b91cfec2095f4d"
PASSWORD = "4fd07a3f"

db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

#this function try if connector is connect if not it reconect db_connection

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = "/static/img/libraries/"
    app.config['SECRET_KEY'] = 'randomKey'

    from .views import views
    app.register_blueprint(views,url_prefix='/')

    from .admin import admin
    app.register_blueprint(admin,url_prefix='/admin/')

    from .auth import auth
    app.register_blueprint(auth,url_prefix='/auth/')

    from .database import database
    app.register_blueprint(database,url_prefix='/database/')
    
    from .librarian import librarySystem
    app.register_blueprint(librarySystem,url_prefix='/librarian/')

    from .distrib import distribSystem
    app.register_blueprint(distribSystem,url_prefix='/distributor/')

    return app