from flask import Blueprint
from . import db_connection

database = Blueprint("database",__name__)


#this function add user to User table
#notes -> you should set role of with setting appropriate optinal argument to True
#      -> in atribute birth_date use function datetime.date(year,month,day)    
def add_user(name,surname,email,birth_date,
             password,admin=False,librarian=False,
             distributor=False,reader=False,unregistered=False):

    query = '''INSERT INTO User(name, surname, email, birth_date, password, admin, librarian, distributor, reader, unregistered) 
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
    to_insert = (name,surname,email,birth_date,password,int(admin),int(librarian),int(distributor),int(reader),int(unregistered))

    cursor = db_connection.cursor()
    cursor.execute(query,to_insert)
    db_connection.commit()
    cursor.close()
