from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'randomKey'

    from .views import views
    app.register_blueprint(views,url_prefix='/')

    from .admin import admin
    app.register_blueprint(admin,url_prefix='/admin/')

    from .auth import auth
    app.register_blueprint(auth,url_prefix='/auth/')

    from .database import database
    app.register_blueprint(database,url_prefix='/database/')
    
    return app