from flask import Blueprint
import mysql.connector as mysql
from . import db_connection, HOST, DATABASE, USER, PASSWORD

database = Blueprint("database",__name__)


#converts array element which has type datetime to date
def convert_datetime_to_date(arr):
        for el in arr:
                el["registration_time"] =  el["registration_time"].date()
        return arr


#takse as input query and input parameters
#this function execute select query and return dict of results
def is_connect():
    global db_connection
    
    if (not db_connection.is_connected()):
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

def execute_select(query,parameters = None):
        is_connect()
        cursor = db_connection.cursor()

        if(parameters != None):
                cursor.execute(query,parameters)
        else:
                cursor.execute(query)

        records = cursor.fetchall()
        columns = [i[0] for i in cursor.description]

        results = []
        for row in records:
                results.append(dict(zip(columns, row)))  

        cursor.close()
        return results

#this function add user to User table
#notes -> you should set role of with setting appropriate optinal argument to True
#      -> in atribute birth_date use function datetime.date(year,month,day)    
def add_user(name,surname,email,birth_date,
        password,admin=False,librarian=False,
        distributor=False,reader=False,unregistered=False):

        query = '''INSERT INTO User(user_name, user_surname, email, birth_date, password, admin, librarian, distributor, reader) 
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
        to_insert = (name,surname,email,birth_date,password,int(admin),int(librarian),int(distributor),int(reader))

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,to_insert)
        db_connection.commit()
        cursor.close()

# this function returns dict of user information in shape {column_name:value}
def get_user_with_this_email(email):

        query = 'SELECT * FROM User WHERE email=%s'
        parameter = tuple([email])

        return convert_datetime_to_date(execute_select(query,parameters=parameter))
        

#this function takes no arguments and returns all titles which are in the system
def db_books():

        query = "SELECT * FROM Book_title"

        return execute_select(query)

#this function takes as input library name
#return dict of books in library
def db_books_in_lib(libraryid):
        query = '''SELECT b.title_id, b.title_name, b.rating, b.path_to_picture ,bl.count FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
                    JOIN Library l ON bl.library_id = l.library_id WHERE l.library_id = %s'''

        parameter = tuple([libraryid])
        return execute_select(query,parameters=parameter)

#this function returns 20 best rewiews books titles
def db_top_books():     
        query = "SELECT title_id,title_name,rating,path_to_picture FROM Book_title GROUP BY rating DESC limit 10"

        return execute_select(query)

#takes as input name of book_title
#returns all informations about this book and also dict of authors 
def db_book_info(title_id):
        query = "SELECT title_name FROM Book_title"
        parameter = tuple([title_id])
        query2 = '''SELECT  b.title_name,b.rating,b.path_to_picture,a.author_name, a.author_surname FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id WHERE b.title_id = %s'''

        return execute_select(query2,parameters=parameter)

def db_book_authors(title_id):
        query2 = '''SELECT a.author_name, a.author_surname FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id WHERE b.title_id = %s'''
        parameter = tuple([title_id])
        return execute_select(query2,parameters=parameter)


def db_all_book_info():
        query2 = '''SELECT  b.title_name,b.rating,b.path_to_picture,a.author_name, a.author_surname FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id GROUP BY b.title_id '''
        return execute_select(query2)

def db_all_book_in_lib(lib_id):
        parameter = tuple([lib_id])
        query = '''SELECT b.title_name,b.rating,b.path_to_picture,a.author_name, a.author_surname  FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
                    JOIN Library l ON bl.library_id = %s join Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id GROUP BY b.title_id '''
        return execute_select(query)

def db_all_book_with_genre(genre_id):
        parameter = tuple([genre_id])
        query = '''SELECT b.title_name,b.rating,b.path_to_picture,a.author_name, a.author_surname  FROM Book_title b JOIN Tag t ON b.title_id = t.title_id 
                    JOIN Genre g ON t.genre_id = %s join Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id GROUP BY b.title_id '''
        return execute_select(query)

def db_book_by_id(book_id):
        query = "SELECT * FROM Book_title b WHERE b.title_id = %s"
        parameter = tuple([book_id])

        return execute_select(query,parameters=parameter)

#takes as input id of user
# returns all reservations from user with this id
def db_reserved_books(user_id):
        query = '''SELECT r.* FROM Reservation r JOIN Book_title b ON r.title_id = b.title_id 
               JOIN User u ON r.creator_id = u.user_id WHERE u.user_id = %s''' 
        
        parameter = tuple([user_id])
        return execute_select(query,parameters=parameter)

#this function returns all libraries in system
def db_libraries():
        query = "SELECT * FROM Library"

        return execute_select(query)

#this function returns counts of given title in each libraries
def db_libraries_with_book(book_name):
        query = '''SELECT l.library_name, count FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
                   JOIN Library l ON bl.library_id = l.library_id WHERE b.title_name = %s'''
        
        parameter = tuple([book_name])
        return execute_select(query,parameters=parameter)

#this function returns all users in system
def get_all_users():
        query = "SELECT * FROM User"

        convert_datetime_to_date(execute_select(query))

# this function takes as input email of user which will be deleted
def delete_user(email):
        param = tuple([email])
        query = "DELETE FROM User WHERE email=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

#this function finds user via mail or name or surname acording to input
def find_user(string_to_find):
        
        param = tuple([string_to_find for i in range(3)])
        query = "SELECT * FROM User WHERE email=%s or user_name=%s or user_surname=%s"

        return convert_datetime_to_date(execute_select(query,parameters=param))

#this function returns book which has this genre
def db_books_with_genre(genre):
        param = tuple([genre])
        query = '''SELECT b.title_id, b.title_name, b.rating, b.path_to_picture FROM  Book_title b JOIN  Tag t ON b.title_id = t.title_id 
                JOIN Genre g ON t.genre_id = g.genre_id WHERE g.genre_id=%s'''

        return execute_select(query,parameters=param)


def db_genres():
        query = '''SELECT * FROM Genre'''
        return execute_select(query)

def db_genre_info(genreid):

        query = '''SELECT * FROM Genre WHERE genre_id=%s'''
        param=tuple([genreid])
        return execute_select(query,parameters=param)

def db_library_info(libid):

        query = '''SELECT library_name FROM Library WHERE library_id=%s'''
        param=tuple([libid])
        return execute_select(query,parameters=param)