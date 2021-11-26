import mysql.connector as mysql
import _datetime as datetime
from random import seed
from random import randint
# Database host info
# HOST = "eu-cdbr-west-01.cleardb.com" 
# DATABASE = "heroku_c8164a0212f5cf6"
# USER = "b91cfec2095f4d"
# PASSWORD = "4fd07a3f"
HOST = None
DATABASE = None
USER = None
PASSWORD = None

db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)


#deleting tables if exists
drop_tables = '''DROP TABLE IF EXISTS Book_title_author;
                 DROP TABLE IF EXISTS Book_title_library;
                 DROP TABLE IF EXISTS Author;
                 DROP TABLE IF EXISTS Book_title;
                 DROP TABLE IF EXISTS Library;
                 DROP TABLE IF EXISTS Tag;
                 DROP TABLE IF EXISTS Genre;
                 DROP TABLE IF EXISTS Lending;
                 DROP TABLE IF EXISTS Order_book;
                 DROP TABLE IF EXISTS Order;
                 DROP TABLE IF EXISTS Publishers;
                 DROP TABLE IF EXISTS Votes;
                 DROP TABLE IF EXISTS User;
                 DROP TABLE IF EXISTS Queue;
                 DROP TABLE IF EXISTS Reservation;
'''

#script for library table
make_library = '''
      CREATE TABLE Library(
      library_id int AUTO_INCREMENT PRIMARY KEY,
      library_name varchar(30) not null,
      library_email varchar(30) not null,
      town VARCHAR(20) NOT NULL,
      adress VARCHAR(50) NOT NULL,              # because can be in shape like 256/22 thats why varchar 
      opening_hours VARCHAR(20),
      description TEXT,
      webpage_link VARCHAR(40),
      path_to_picture VARCHAR(35)
      )
'''

#script for library table
make_genre = '''
      CREATE TABLE Genre(
      genre_id int AUTO_INCREMENT PRIMARY KEY,
      genre_name varchar(30) not null
      )
'''

#script for table which represent bindings with book_title and library
make_book_title_genre = '''
      CREATE TABLE Tag(
      title_id int not null,
      genre_id int not null,
      CONSTRAINT tag_title foreign key (title_id) references Book_title(title_id),
      CONSTRAINT tag_genre foreign key (genre_id) references Genre(genre_id),
      CONSTRAINT tag_unique UNIQUE (title_id, genre_id)
      )
'''

make_order = '''CREATE TABLE Orders(
      order_id int AUTO_INCREMENT PRIMARY KEY,
      librarian_id int not NULL,
      distributor_id int not NULL,
      CONSTRAINT order_librarian foreign key (librarian_id) references User(user_id) ON DELETE CASCADE,
      CONSTRAINT order_distributor foreign key (distributor_id) references Publishers(publisher_id) ON DELETE CASCADE
      )
'''

make_order_book = '''CREATE TABLE Order_book(
      title_id int not NULL,
      order_id int not NULL,
      count int not null,
      CONSTRAINT order_title foreign key (title_id) references Book_title(title_id) ON DELETE CASCADE,
      CONSTRAINT order_book foreign key (order_id) references Orders(order_id) ON DELETE CASCADE,
      CONSTRAINT order_unique UNIQUE (title_id, order_id)
      )
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
      title_name VARCHAR(40) NOT NULL,
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
      CONSTRAINT title_library_title foreign key (title_id) references Book_title(title_id) ON DELETE CASCADE,
      CONSTRAINT title_library_library foreign key (library_id) references Library(library_id) ON DELETE CASCADE,
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
      author_name VARCHAR(20) NOT NULL,
      author_surname VARCHAR(20) NOT NULL
      )
'''


''

make_book_queue= '''
      CREATE TABLE Queue(
      title_id int not null,
      user_id int not null,
      library_id int not null,
      time TIMESTAMP not null,
      CONSTRAINT queue_title key (title_id) references Book_title(title_id) ON DELETE CASCADE,
      CONSTRAINT queue_user foreign key (user_id) references User(user_id) ON DELETE CASCADE,
      CONSTRAINT queue_library foreign key (library_id) references Library(library_id) ON DELETE CASCADE,
      CONSTRAINT queue_library_user_title UNIQUE (title_id, user_id,library_id)
      )
'''


#script for table which represent bindings with book_title and library
make_book_title_author = '''
      CREATE TABLE Book_title_author(
      title_id int not null,
      author_id int not null,
      CONSTRAINT title_author_title foreign key (title_id) references Book_title(title_id) ON DELETE CASCADE,
      CONSTRAINT title_author_author foreign key (author_id) references Author(author_id) ON DELETE CASCADE,
      CONSTRAINT title_author_unique UNIQUE (title_id, author_id)
      )
'''
insert_Book_title_author= '''INSERT INTO Book_title_author(title_id,author_id) 
                    VALUES(%s, %s)
'''

#script for table which represent bindings with book_title and library
make_user = '''
      CREATE TABLE User(
      user_id int AUTO_INCREMENT PRIMARY KEY,
      user_name VARCHAR(20) not null,
      user_surname VARCHAR(20) not null,
      email VARCHAR(30) not null,
      birth_date DATE not null,
      password VARCHAR(300),
      admin BOOLEAN,
      librarian BOOLEAN,
      distributor BOOLEAN,
      reader BOOLEAN,
      library_id int,
      publisher_id int,
      CONSTRAINT fk_user foreign key (library_id) references Library(library_id) ON DELETE CASCADE,
      CONSTRAINT fk_user foreign key (publisher_id) references Publishers(publisher_id) ON DELETE CASCADE,
      )
'''
insert_user = '''INSERT INTO User(name,surname,email,birth_date,password,admin,librarian,distributor,reader,unregistered,library_id) 
                    VALUES(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
'''

#script for table which represent bindings with book_title and library
make_reservation = '''
      CREATE TABLE Reservation(
      reservation_id int AUTO_INCREMENT PRIMARY KEY,
      time TIMESTAMP not null,
      until Date not null,
      title_id int not null,
      creator_id int not null,
      handler_id int ,
      CONSTRAINT reservation_title foreign key (title_id) references Book_title(title_id) ON DELETE CASCADE,
      CONSTRAINT reservation_creator foreign key (creator_id) references User(user_id) ON DELETE CASCADE,
      CONSTRAINT reservation_handler foreign key (handler_id) references User(user_id) ON DELETE CASCADE
      )
'''

make_publishers = '''
      CREATE TABLE Publishers(
      publisher_id int AUTO_INCREMENT PRIMARY KEY,
      publisher_name varchar(50) not null,
      publisher_email varchar(50) not null,
      adress varchar(50) not null,
      town varchar(50) not null
      )
'''





#script for table which represent bindings with book_title and library
make_lending = '''
      CREATE TABLE Lending(
      lending_id int AUTO_INCREMENT PRIMARY KEY,
      when_borowed TIMESTAMP not null,
      until DATE not null,
      time_of_lending int not null,
      title_id int not null,
      customer_id int not null,
      handler_id int,
      CONSTRAINT lending_title foreign key (title_id) references Book_title(title_id) ON DELETE CASCADE,
      CONSTRAINT lending_creator foreign key (customer_id) references User(user_id) ON DELETE CASCADE,
      CONSTRAINT lending_handler foreign key (handler_id) references User(user_id) ON DELETE CASCADE
      )
'''



make_votes = '''
      CREATE TABLE Votes(
      title_id int not null,
      library_id int not null,
      user_id int not null,
      yes boolean,
      no boolean,
      CONSTRAINT votes_title foreign key (title_id) references Book_title(title_id) ON DELETE CASCADE,
      CONSTRAINT votes_library foreign key (library_id) references Library(library_id) ON DELETE CASCADE,
      CONSTRAINT votes_user foreign key (user_id) references User(user_id) ON DELETE CASCADE,
      CONSTRAINT votes_user_library_title_unique UNIQUE (title_id, library_id, user_id) ON DELETE CASCADE
      )
'''







####### boook title library inserting ##############

#seed(1)

# generate some integers
'''
for i in range(0,6):
      tmp = []
      library_id = (i * 10 + 5)
      for _ in range(15):
            query = "INSERT INTO `book_title_library` (`title_id`, `library_id`, `count`) VALUES (%s, %s, %s)"
            book_id = randint(0, 23) * 10 + 5
            while(book_id in tmp):
                  book_id = randint(0, 23) * 10 + 5
            tmp.append(book_id)
            count = randint(1, 100)
            x = [book_id,library_id,count]
            parameter = tuple(x)
            cursor = db_connection.cursor()
            cursor.execute(query,parameter)
            db_connection.commit()
            cursor.close()
'''

#generate authors
'''
names = ["George", "Bella","Terry", "Ryan"," Catherine", "Michelle", "Meghan", "Aidan", "Daniella", "Mason", "Carmen", "Elijah", "Freddie", "Felicity", "Felix"]
surnames = ["Stewart", "Taylor", "Brown", "Williams", "Lewis", "Smith", "Johnson", "Thomas", "Evans", "Wilson", "Roberts", "Jones", "Davies", "Thompson", "Robinson"]


for i in range (0,30):
      query = "INSERT INTO `author` (`author_id`, `name`, `surname`) VALUES (NULL, %s, %s)"
      name = names[randint(0,14)]
      surname = surnames[randint(0,14)]
      x = [name,surname]
      parameter = tuple(x)
      cursor = db_connection.cursor()
      cursor.execute(query,parameter)
      db_connection.commit()
      cursor.close()
db_connection.close()


for i in range(0,26):
      cursor = db_connection.cursor()
      book_id = (i * 10 + 5)
      author_id = randint(0, 23) * 10 + 5
      x = [book_id,author_id]
      parameter = tuple(x)
      query = "INSERT INTO `book_title_author` (`title_id`, `author_id`) VALUES (%s, %s)"
      cursor.execute(query,parameter)
      db_connection.commit()
      if(i %3 == 0):
            while(True):
                  tmp = randint(0, 23) * 10 + 5
                  print(author_id,tmp)
                  if author_id != tmp:
                        break
            x = [book_id,tmp]
            parameter = tuple(x)
            cursor.execute(query,parameter)
            db_connection.commit()
      if(i %9 == 0):
            while(True):
                  tmp2 = randint(0, 23) * 10 + 5
                  if tmp2 != tmp and tmp2 != author_id:
                        break
            x = [book_id,tmp2]
            parameter = tuple(x)
            cursor.execute(query,parameter)
            db_connection.commit()
      cursor.close()

'''

#param = tuple(["gorcak.damian@tmp.sk"])
cursor = db_connection.cursor()
cursor.execute(drop_tables)
cursor.execute(make_library)
cursor.execute(make_book_title)
cursor.execute(make_author)
cursor.execute(make_book_title_author)
cursor.execute(make_book_title_library)
cursor.execute(make_genre)
cursor.execute(make_book_title_genre)
cursor.execute(make_publishers)
cursor.execute(make_user)
cursor.execute(make_lending)
cursor.execute(make_reservation)
cursor.execute(make_votes)
cursor.execute(make_book_queue)
cursor.execute(make_order)
cursor.execute(make_order_book)

db_connection.close()
cursor.close()