from random import paretovariate
from flask import Blueprint
import mysql.connector as mysql
from . import db_connection, HOST, DATABASE, USER, PASSWORD

database = Blueprint("database",__name__)


#converts array element which has type datetime to date
def convert_datetime_to_date(arr):
        for el in arr:
                el["registration_time"] =  el["registration_time"].date()
        return arr

def decide(old,new):
        if new == None or new == "":
                return old
        else:
                return new

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
def db_user_info(user_pk):
        query = '''SELECT * FROM user where user_id = %s;'''
        parameter = tuple([user_pk])
        return execute_select(query,parameters=parameter)

# this function returns dict of user information in shape {column_name:value}
def get_user_with_this_email(email):

        query = 'SELECT * FROM User WHERE email=%s'
        parameter = tuple([email])

        return convert_datetime_to_date(execute_select(query,parameters=parameter))
        

#this function takes no arguments and returns all titles which are in the system
def db_insert_book(release_date,isbn,rating,description,path_to_picture,title_name,publisher_id):
        query = '''INSERT INTO book_title(release_date,isbn,rating,description,path_to_picture,title_name,publisher_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s);'''
        parameter = tuple([release_date,isbn,rating,description,path_to_picture,title_name,publisher_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        id_of_book = cursor.lastrowid
        db_connection.commit()
        cursor.close()
        return id_of_book

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
        query2 = '''SELECT b.*,a.author_name, a.author_surname FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id WHERE b.title_id = %s'''

        return execute_select(query2,parameters=parameter)

def db_book_authors(title_id):
        query2 = '''SELECT a.author_name, a.author_surname,a.author_id FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id WHERE b.title_id = %s'''
        parameter = tuple([title_id])
        return execute_select(query2,parameters=parameter)

def db_authors():
        query = '''SELECT author_name, author_surname, author_id FROM Author;'''
        return execute_select(query)

def db_add_author(name,last_name):
        query = '''INSERT INTO author(author_name,author_surname) VALUES (%s,%s);'''
        parameter=tuple([name,last_name])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        id_of_author = cursor.lastrowid
        db_connection.commit()
        cursor.close()
        return id_of_author

def db_add_book_author(title_id,author_id):
        query = '''INSERT INTO book_title_author(title_id,author_id) VALUES (%s,%s);'''
        parameter=tuple([title_id,author_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        db_connection.commit()
        cursor.close()


def db_all_book_info():
        query2 = '''SELECT  b.title_id,b.title_name,b.rating,b.path_to_picture,a.author_name, a.author_surname FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id GROUP BY b.title_id '''
        return execute_select(query2)

def db_all_book_in_lib(lib_id):
        parameter = tuple([lib_id])
        query = '''SELECT b.title_id,b.title_name,b.rating,b.path_to_picture,a.author_name, a.author_surname  FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
                    JOIN Library l ON bl.library_id = %s join Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id GROUP BY b.title_id '''
        return execute_select(query,parameters=parameter)

def db_all_books_not_in_lib(lib_id):
        #query = '''SELECT b.title_id, b.title_name FROM book_title b JOIN book_title_library bl ON b.title_id = bl.title_id WHERE bl.library_id <> %s;'''
        query = '''select title_name,title_id from Book_title where title_name not in (SELECT b.title_name FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id JOIN Library l ON bl.library_id = l.library_id  Where l.library_id = %s)'''
        parameter = tuple([lib_id])
        return execute_select(query,parameter)

def db_delete_votes(title_id,lib_id):
        query = '''DELETE FROM votes WHERE title_id = %s AND library_id = %s;'''
        parameter=tuple([title_id,lib_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        db_connection.commit()
        cursor.close()

def db_all_book_with_genre(genre_id):
        parameter = tuple([genre_id])
        query = '''SELECT b.title_id,b.title_name,b.rating,b.path_to_picture,a.author_name, a.author_surname  FROM Book_title b JOIN Tag t ON b.title_id = t.title_id 
                    JOIN Genre g ON t.genre_id = %s join Book_title_author ba ON b.title_id = ba.title_id 
                    JOIN Author a ON ba.author_id = a.author_id GROUP BY b.title_id '''
        return execute_select(query,parameters=parameter)

def db_book_by_id(book_id):
        query = "SELECT title_name FROM Book_title b WHERE b.title_id = %s"
        parameter = tuple([book_id])

        return execute_select(query,parameters=parameter)
def db_insert_new_vote(title_id,library_id,user_id):
        query = '''INSERT INTO votes(title_id,library_id,user_id,yes,no) VALUES (%s, %s, %s, 1, 0)'''
        parameter=tuple([title_id,library_id,user_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        db_connection.commit()
        cursor.close()

def db_votes_for_user_lib(user_id,lib_id,title_id):
        query = '''SELECT * FROM votes WHERE user_id = %s AND library_id = %s AND title_id = %s;'''
        parameter = tuple([user_id,lib_id,title_id])
        return execute_select(query,parameter)
def db_votes_in_library(lib_id):
        query = '''SELECT v.title_id, b.title_name FROM votes v JOIN book_title b ON v.title_id = b.title_id WHERE v.library_id = %s;'''
        parameter = tuple([lib_id])
        return execute_select(query,parameter)
#takes as input id of user
# returns all reservations from user with this id
def db_reserved_books(user_id):
        query = '''SELECT r.*, b.title_name, l.library_name FROM Reservation r JOIN Book_title b ON r.title_id = b.title_id 
               JOIN User u ON r.user_id = u.user_id JOIN Library l ON l.library_id = r.library_id WHERE u.user_id = %s''' 
        
        parameter = tuple([user_id])
        return execute_select(query,parameters=parameter)

#this function returns all libraries in system
def db_libraries():
        query = "SELECT * FROM Library"

        return execute_select(query)

#this function returns counts of given title in each libraries
def db_libraries_with_book(title_id):
        query = '''SELECT l.library_id,l.library_name, count FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
                   JOIN Library l ON bl.library_id = l.library_id WHERE b.title_id = %s'''
        
        parameter = tuple([title_id])
        return execute_select(query,parameters=parameter)

#this function returns all users in system
def get_all_users():
        query = "SELECT * FROM User"

        return convert_datetime_to_date(execute_select(query))

# this function takes as input email of user which will be deleted
def delete_user(email):
        param = tuple([email])
        query = "DELETE FROM User WHERE email=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def db_delete_book(bookid,library_id):
        query = '''DELETE FROM book_title_library WHERE title_id = %s AND library_id = %s;'''
        param = tuple([bookid,library_id])
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

def find_library(string_to_find):
        
        param = tuple([string_to_find for i in range(3)])
        query = "SELECT * FROM Library WHERE library_email=%s or library_name=%s or town = %s"

        return execute_select(query,parameters=param)

def find_distributors(string_to_find):
        
        param = tuple([string_to_find for i in range(3)])
        query = "SELECT * FROM Publishers WHERE publisher_email=%s or publisher_name=%s or town = %s"

        return execute_select(query,parameters=param)

def db_counts_of_books_in_library(lib_pk):
        query = '''SELECT count FROM book_title_library WHERE library_id = %s'''
        parameter = tuple([lib_pk])
        return execute_select(query,parameters=parameter)
        
#this function returns book which has this genre
def db_books_with_genre(genre):
        param = tuple([genre])
        query = '''SELECT b.title_id, b.title_name, b.rating, b.path_to_picture FROM  Book_title b JOIN  Tag t ON b.title_id = t.title_id 
                JOIN Genre g ON t.genre_id = g.genre_id WHERE g.genre_id=%s'''

        return execute_select(query,parameters=param)
def db_update_rating(title_id,new_value):
        query = '''UPDATE book_title SET rating = %s WHERE title_id = %s;'''
        parameter = tuple([new_value,title_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_update_book(title_id,title_name,description,release_date,isbn):
        query = '''UPDATE book_title SET title_name = %s, description = %s,release_date = %s,ISBN = %s WHERE title_id = %s;'''
        parameter = tuple([title_name,description,release_date,isbn,title_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_delete_book_author(title_id,author_id):
        query = "DELETE FROM book_title_author WHERE title_id = %s AND author_id = %s"
        param = tuple([title_id,author_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def db_update_book_path_to_picture(title_id,path_to_picture):
        query = '''UPDATE book_title SET path_to_picture = %s WHERE title_id = %s;'''
        parameter = tuple([path_to_picture,title_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_genres():
        query = '''SELECT * FROM Genre'''
        return execute_select(query)

def db_genre_info(genreid):

        query = '''SELECT * FROM Genre WHERE genre_id=%s'''
        param=tuple([genreid])
        return execute_select(query,parameters=param)

def db_library_info(libid):
        query = '''SELECT library_name,library_id FROM Library WHERE library_id=%s'''

        param=tuple([libid])
        return execute_select(query,parameters=param)

def db_selected_genres(title_id):
        query = '''SELECT genre_id FROM tag WHERE title_id = %s'''
        param=tuple([title_id])
        return execute_select(query,parameters=param)

def db_add_genre_to_book(genre_id,title_id):
        query = '''INSERT INTO tag (title_id,genre_id) VALUES (%s,%s);'''
        parameter=tuple([title_id,genre_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        db_connection.commit()
        cursor.close()

def db_delete_genre_to_book(genre_id,title_id):
        query = '''DELETE FROM tag WHERE genre_id = %s AND title_id = %s'''
        parameter=tuple([genre_id,title_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        db_connection.commit()
        cursor.close()

#this function updates user table
def update_user_db(atributes):
        query = '''UPDATE `user` SET `library_id` = %s,`user_name` = %s, `user_surname` = %s, `email` = %s,`birth_date` = %s, `admin` = %s, `librarian` = %s, `distributor` = %s, `reader` = %s WHERE `user`.`email` = %s'''

        original_values = get_user_with_this_email(atributes["old_email"])[0]
        
        if(int(atributes["library_id"]) == 0):       
                lib_id =  original_values["library_id"]
        else:
                lib_id = atributes["library_id"]

        x = [lib_id,
             decide(original_values["user_name"],atributes["user_name"]),
             decide(original_values["user_surname"],atributes["user_surname"]),
             decide(original_values["email"],atributes["email"]),
             decide(original_values["birth_date"],atributes["birth_date"]),
             decide(original_values["admin"],atributes["admin"]),
             decide(original_values["librarian"],atributes["librarian"]) ,  
             decide(original_values["distributor"],atributes["distributor"]) ,  
             decide(original_values["reader"],atributes["reader"]) ,
             atributes["old_email"]
             ]

        
        
        parameter = tuple(x)
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_reservations_in_lib(lib_pk):
        query = '''SELECT u.user_id,u.email,b.title_id,b.title_name,r.time,r.reservation_id, r.until from Reservation r 
                   join Library l on %s = r.library_id join User u on 
                   u.user_id = r.user_id join Book_title b on r.title_id = b.title_id  GROUP BY r.reservation_id'''
        param=tuple([lib_pk])
        return execute_select(query,parameters=param)

def db_reservation_info(res_pk):
        query = '''SELECT * FROM Reservation WHERE reservation_id = %s;'''
        param=tuple([res_pk])
        return execute_select(query,parameters=param)

def db_remove_reservation(res_pk):
        param = tuple([res_pk])
        query = "DELETE FROM Reservation WHERE reservation_id=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def db_update_reservation_time(res_pk,time):
        query = '''UPDATE `Reservation` SET `until` = %s WHERE `reservation`.`reservation_id` = %s'''

        x = [time,res_pk]
        parameter = tuple(x)

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_actual_count(lib_pk,book_pk):
        query = '''SELECT count FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
                JOIN Library l ON bl.library_id = l.library_id WHERE b.title_id = %s and l.library_id = %s'''

        x = [book_pk,lib_pk]
        param=tuple(x)
        return execute_select(query,parameters=param)

def db_insert_new_count(title_id,library_id,count):
        query = '''INSERT INTO book_title_library (title_id,library_id,count) VALUES (%s,%s,%s);'''
        parameter=tuple([title_id,library_id,count])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        db_connection.commit()
        cursor.close()

def db_update_actual_count(new_count,lib_pk,book_pk):
        query = '''UPDATE Book_title_library SET count = %s WHERE title_id = %s and library_id = %s '''

        x = [new_count,book_pk,lib_pk]
        parameter = tuple(x)

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)

        db_connection.commit()
        cursor.close()



#until = datetime.date()
def db_insert_borrow(until,title_id,customer_id,handler_id,library_id):
        query = '''INSERT INTO `lending` (`until`, `title_id`, `customer_id`, `handler_id`, `library_id`) 
                    VALUES (%s, %s, %s, %s, %s);'''
        
        x = [until,title_id,customer_id,handler_id,library_id]
        parameter = tuple(x)

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_update_borrow_time(res_pk,time):
        query = '''UPDATE `lending` SET `until` = %s WHERE `lending`.`lending_id` = %s'''

        x = [time,res_pk]
        parameter = tuple(x)

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_borrowed_in_lib(lib_pk):
        query = '''SELECT u.user_id,u.email,b.title_id,b.title_name,le.until,le.lending_id from lending le 
                   join Library l on %s = le.library_id join User u on 
                   u.user_id = le.customer_id join Book_title b on le.title_id = b.title_id  GROUP BY le.lending_id'''

        parameter=tuple([lib_pk])
        return execute_select(query,parameters=parameter)

def db_borrowed_books(user_pk):
        query = '''SELECT le.*, b.title_name, l.library_name FROM lending le JOIN Book_title b ON le.title_id = b.title_id 
               JOIN User u ON le.customer_id = u.user_id JOIN Library l ON l.library_id = le.library_id WHERE u.user_id = %s''' 
        parameter = tuple([user_pk])
        return execute_select(query,parameters=parameter)

def db_borrow_info(borrow_id):
        query = '''SELECT * FROM lending WHERE lending_id = %s'''
        parameter = tuple([borrow_id])
        return execute_select(query,parameters=parameter)

def db_insert_reservation(until,title_id,user_id,library_id):
        query = '''INSERT INTO `Reservation` (`until`, `title_id`, `user_id`,`library_id`) 
                    VALUES (%s, %s, %s, %s);'''
        
        x = [until,title_id,user_id,library_id]
        parameter = tuple(x)

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_res_with_book_lib_user(titleid,userid,libid):
        query = '''SELECT * FROM `Reservation` WHERE title_id = %s AND user_id = %s AND library_id = %s;'''
        params = tuple([titleid,userid,libid])
        return execute_select(query,parameters=params)

def db_bor_with_book_lib_user(titleid,userid,libid):
        query = '''SELECT * FROM `lending` WHERE title_id = %s AND lending_id = %s AND library_id = %s;'''
        params = tuple([titleid,userid,libid])
        return execute_select(query,parameters=params)

def db_remove_borrow(bor_pk):
        param = tuple([bor_pk])
        query = "DELETE FROM lending WHERE lending_id=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def db_borrow_info(bor_pk):
        query = '''SELECT * FROM lending WHERE lending_id = %s;'''
        params = tuple([bor_pk])
        return execute_select(query,parameters=params)

def find_similar_genre_book(title_id):
        query = '''SELECT b.title_id, b.title_name,b.rating,b.path_to_picture FROM  Book_title b JOIN tag t ON b.title_id = t.title_id 
              JOIN genre g ON g.genre_id = t.genre_id WHERE g.name = (SELECT g.name FROM  Book_title b JOIN 
              tag t ON b.title_id = t.title_id 
              JOIN genre g ON g.genre_id = t.genre_id WHERE b.title_id = %s LIMIT 1) limit 5'''
        
        param = tuple([title_id])
        return execute_select(query,parameters=param)

def add_to_queue(book_id,lib_id,user_id):
        query = '''INSERT INTO `queue` (`title_id`, `user_id`, `library_id`, `time`) 
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP);'''
        x = book_id,lib_id,user_id
        param = tuple(x)
        
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)

        db_connection.commit()
        cursor.close()

def db_remove_from_queue(book_id,lib_id,user_id):
        x = book_id,lib_id,user_id
        param = tuple(x)
        query = "DELETE FROM Queue WHERE title_id=%s and user_id = %s and library_id = %s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def db_distributor_info(distrib_pk):
        query = '''SELECT * FROM publishers WHERE publisher_id = %s'''
        parameter = tuple([distrib_pk])
        return execute_select(query,parameters=parameter)

def db_publishers():
        query = '''SELECT * FROM publishers'''
        return execute_select(query)

def db_book_by_publisher(pub_id):
        query = '''SELECT title_id, title_name FROM Book_title WHERE publisher_id=%s;'''
        parameter = tuple([pub_id])
        return execute_select(query,parameters=parameter)

def add_order(lib_id,pub_id):
        query = '''INSERT INTO orders(librarian_id,distributor_id) 
               VALUES(%s, %s)'''
        parameter=tuple([lib_id,pub_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        idOfOrder = cursor.lastrowid
        db_connection.commit()
        cursor.close()
        return idOfOrder

def db_make_order_done(order_id):
        query = '''UPDATE orders SET state = 1 WHERE order_id = %s;'''
        parameter = tuple([order_id])
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        db_connection.commit()
        cursor.close()


def add_books_to_order(order_id,title_ids,counts):
        query = 'INSERT INTO order_book(title_id,order_id,count) VALUES '
        values = ",".join([f'({title_ids[i]},{order_id},{counts[i]})' for i in range(len(title_ids))])
        query = f'{query}{values};'

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query)
        db_connection.commit()
        cursor.close()

def db_unfinished_orders_for_distributor(distrib_id):
        query = '''SELECT o.*,u.email FROM orders o JOIN user u ON u.user_id = o.librarian_id WHERE distributor_id = %s AND state = 0;'''
        parameter = tuple([distrib_id])
        return execute_select(query,parameter)

def db_info_about_books_in_order(order_id):
        query = '''SELECT b.title_id, b.title_name, o.count FROM order_book o JOIN book_title b ON o.title_id = b.title_id WHERE o.order_id = %s'''
        parameter = tuple([order_id])
        return execute_select(query,parameter)

def db_order_info(order_id):
        query = '''SELECT * FROM orders WHERE order_id = %s;'''
        parameter = tuple([order_id])
        return execute_select(query,parameters=parameter)

def delete_library(lib_id):
        param = tuple([lib_id])
        query = "DELETE FROM Library WHERE library_id=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def db_books_with_publisher(pub_id):
        query = '''SELECT * FROM book_title WHERE publisher_id = %s;'''
        parameter = tuple([pub_id])
        return execute_select(query,parameters=parameter)

#this function updates user table
def update_lib_db(atributes):
        query = '''UPDATE `Library` SET `library_name` = %s, `opening_hours` = %s,`webpage_link` = %s, `library_email` = %s WHERE `library_email` = %s'''

        original_values = find_library(atributes["old_email"])[0]
       
        x = [decide(original_values["library_name"],atributes["library_name"]),
             decide(original_values["opening_hours"],atributes["opening_hours"]),
             decide(original_values["webpage_link"],atributes["webpage_link"]),
             decide(original_values["library_email"],atributes["library_email"]),
             atributes["old_email"]
             ]

        parameter = tuple(x)
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

#this function updates user table
def update_distributor_db(atributes):
        query = '''UPDATE `Publishers` SET `publisher_name` = %s, `publisher_email` = %s, `adress` = %s,`town` = %s WHERE `Publishers`.`publisher_id` = %s'''

        original_values = find_distributors(atributes["old_email"])[0]
        
        x = [decide(original_values["publisher_name"],atributes["publisher_name"]),
             decide(original_values["publisher_email"],atributes["publisher_email"]),
             decide(original_values["adress"],atributes["adress"]),
             decide(original_values["town"],atributes["town"]),
             original_values["publisher_id"]
             ]

        
        
        parameter = tuple(x)
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def db_distributors():
        query = '''SELECT * FROM Publishers'''

        return execute_select(query)

def delete_distributors(dist_email):
        param = tuple([dist_email])
        query = "DELETE FROM Publishers WHERE publisher_email=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def db_tags(tag=None):
        if(tag == None):
                query = '''SELECT * FROM Genre'''
                return execute_select(query)
        else:
                query = '''SELECT * FROM Genre where genre_id = %s'''
                param = tuple([tag])
                return execute_select(query,parameters=param)

def delete_tag(tag_id):
        param = tuple([tag_id])
        query = "DELETE FROM Genre WHERE genre_id=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def insert_tag(tag_name):
        if(tag_name["name"] == "" or tag_name["name"] == None):
                return False
        
        param = tuple([tag_name["name"]])
        query = "INSERT INTO Genre(name) VALUES (%s)"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()
        return True

def update_tag_db(name):
        query = '''UPDATE `Genre` SET `name` = %s WHERE `genre_id` = %s'''        
        x = [name["name"],name["genre_id"]]
        parameter = tuple(x)
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,parameter)
        
        db_connection.commit()
        cursor.close()

def delete_library(lib_email):
        param = tuple([lib_email])
        query = "DELETE FROM Library WHERE library_email=%s"

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        
        db_connection.commit()
        cursor.close()

def insert_into_lib(atributes):
        lib = atributes
        
        lib_name = lib['library_name']
        town = lib['town']
        opening_hours = lib['opening_hours']
        description = lib['description']
        link = lib['webpage_link']
        path_to_picture = lib['path_to_picture']
        lib_email = lib['library_email']
        adress = lib['adress']

        x = [lib_name,town,opening_hours,description,
             link,path_to_picture,lib_email,adress]

        if("" in x):
                return False

        param = tuple(x)
        query = '''INSERT INTO `library` (`library_name`, `town`, `opening_hours`, `description`,
                 `webpage_link`, `path_to_picture`, `library_email`, `adress`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        db_connection.commit()
        cursor.close()
        return True

def insert_into_dist(dist):
        
        x = [dist["publisher_name"],dist["publisher_email"],dist["adress"],dist["town"]]

        param = tuple(x)
        query = '''INSERT INTO `Publishers` (`publisher_name`, `publisher_email`, `adress`, `town`) 
                VALUES (%s, %s, %s, %s);'''

        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        db_connection.commit()
        cursor.close()

def distributor_alma_mater(dist_id):
        query = '''select p.publisher_id from Publishers p  JOIN User u  ON u.publisher_id = p.publisher_id 
                        where u.email = %s'''
        param = tuple([dist_id])
        
        return execute_select(query,parameters=param)

def add_publisher_to_dist(dic):
        if(dic['publisher_id'] != '0'):
                print("som tu")
                query = '''Update User set publisher_id = %s where email = %s'''
                x = [dic["publisher_id"],dic["old_email"]]
        else:
                query = '''Update User set publisher_id = NULL where email = %s'''
                x = [dic["old_email"]]
        param = tuple(x)
        
        is_connect()
        cursor = db_connection.cursor()
        cursor.execute(query,param)
        db_connection.commit()
        cursor.close()