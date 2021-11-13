import mysql.connector as mysql
import _datetime as datetime
HOST = "sql11.freesqldatabase.com" 
DATABASE = "sql11449509"
USER = "sql11449509"
PASSWORD = "1JR1eSrwxJ"

db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
cursor = db_connection.cursor()

#deleting tables if exists
drop_tables = '''DROP TABLE IF EXISTS Book_title_author;
                 DROP TABLE IF EXISTS Book_title_library;
                 DROP TABLE IF EXISTS Author;
                 DROP TABLE IF EXISTS Book_title;
                 DROP TABLE IF EXISTS Library;
'''

#script for library table
make_library = '''
      CREATE TABLE Library(
      library_id int AUTO_INCREMENT PRIMARY KEY,
      town VARCHAR(20) NOT NULL,
      street VARCHAR(20) NOT NULL,
      house_number VARCHAR(20) NOT NULL,              # because can be in shape like 256/22 thats why varchar 
      opening_hours VARCHAR(20),
      description TEXT,
      webpage_link VARCHAR(40),
      path_to_picture VARCHAR(35)
      )
'''
insert_library = '''INSERT INTO Library(town,street,house_number,opening_hours,description,webpage_link,path_to_picture) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
'''

#script for book title table
make_book_title = '''
      CREATE TABLE Book_title(
      title_id int AUTO_INCREMENT PRIMARY KEY,
      release_date DATE NOT NULL,
      ISBN VARCHAR(20) NOT NULL,
      rating float,
      description TEXT,
      path_to_picture VARCHAR(35),
      name VARCHAR(40) NOT NULL,
      )
'''

insert_Book_title = '''INSERT INTO Book_title(release_date,ISBN,rating,description,path_to_picture,name) 
                    VALUES(%s, %s, %s, %s, %s,%s)
'''

#script for table which represent bindings with book_title and library
make_book_title_library = '''
      CREATE TABLE Book_title_library(
      title_id int not null,
      library_id int not null,
      count int,
      CONSTRAINT title_library_title foreign key (title_id) references Book_title(title_id),
      CONSTRAINT title_library_library foreign key (library_id) references Library(library_id),
      CONSTRAINT title_library_unique UNIQUE (title_id, library_id)
      )
'''

insert_Book_title_library = '''INSERT INTO Book_title_library(title_id,library_id,count) 
                    VALUES(%s, %s, %s)
'''

#script for creating author
make_author = '''
      CREATE TABLE Author(
      author_id int AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(20) NOT NULL,
      surname VARCHAR(20) NOT NULL
      )
'''

insert_author = '''INSERT INTO Author(name,surname) 
                   VALUES(%s, %s)
'''

#script for table which represent bindings with book_title and library
make_book_title_author = '''
      CREATE TABLE Book_title_author(
      title_id int not null,
      author_id int not null,
      CONSTRAINT title_author_title foreign key (title_id) references Book_title(title_id),
      CONSTRAINT title_author_author foreign key (
      ) references Author(author_id),
      CONSTRAINT title_author_unique UNIQUE (title_id, author_id)
      )
'''
insert_Book_title_author= '''INSERT INTO Book_title_author(title_id,author_id) 
                    VALUES(%s, %s)
'''

sql = '''select *
from tmp2 u join tmp s on u.id = s.id and u.id = 2;
'''

'''
cursor.execute(drop_tables,multi=True)
cursor.execute(make_book_title)
cursor.execute(make_book_title_library)
cursor.execute(make_author)
cursor.execute(make_book_title_author)

to_insert = ("Praha","Brnenska","521/24","08:00 - 17:00",
                    "Lorem Ipsum is simply dummy text of the printing and typesetting industry",
                    "https://www.facebook.com","/static/img/JMENO_SOUBORU")
cursor.execute(insert_library,to_insert)
db_connection.commit()

to_insert = (datetime.date(2021, 3, 23),"9788055180175",8.9,
                    "Kniha Prezident – Dvadsať dní na prežite opisuje strhujúci súboj novozvoleného prezidenta s premiérom, ktorého prezidentské ambície ostali nenaplnené."
                    ,"/static/img/JMENO_SOUBORU","Prezident")
cursor.execute(insert_Book_title,to_insert)
db_connection.commit()

to_insert = (datetime.date(2021, 9, 11),"9788055907475",5.9,
                    "Petra Vlhová a ľudia, ktorí stáli pri nej, opisujú cestu na lyžiarsky vrchol. V súčasnosti najúspešnejšia slovenská športovkyňa vydáva oficiálnu autobiografiu. "
                   ,"/static/img/JMENO_SOUBORU","Petra")
cursor.execute(insert_Book_title,to_insert)
db_connection.commit()


to_insert = (1,3,100)
cursor.execute(insert_Book_title_library,to_insert)
db_connection.commit()

to_insert = (2,4,20)
cursor.execute(insert_Book_title_library,to_insert)
db_connection.commit()

to_insert = (1,4,130)
cursor.execute(insert_Book_title_library,to_insert)
db_connection.commit()


to_insert = ("Damian","Gorcak")
cursor.execute(insert_author,to_insert)
db_connection.commit()

to_insert = ("Jan","Homola")
cursor.execute(insert_author,to_insert)
db_connection.commit()

to_insert = ("Tomas","Krivanek")
cursor.execute(insert_author,to_insert)
db_connection.commit()


to_insert = (2,1)
cursor.execute(insert_Book_title_author,to_insert)
db_connection.commit()
'''
 ## authors of book
#cursor.execute('''SELECT a.name FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
#               JOIN Author a ON ba.author_id = a.author_id WHERE b.name = "Prezident"''')

## how many books on library
#cursor.execute('''SELECT count FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
#               JOIN Library l ON bl.library_id = l.library_id WHERE b.name = "Prezident" and l.town = "Brno"''')
#

records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)

print(records)
print("Connected to:", db_connection.get_server_info())

db_connection.close()
cursor.close()
# enter your code here!