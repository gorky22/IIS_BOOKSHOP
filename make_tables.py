import mysql.connector as mysql
import _datetime as datetime
from random import seed
from random import randint

HOST = "eu-cdbr-west-01.cleardb.com" 
DATABASE = "heroku_c8164a0212f5cf6"
USER = "b91cfec2095f4d"
PASSWORD = "4fd07a3f"

db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)


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
      name varchar(30) not null,
      town VARCHAR(20) NOT NULL,
      street VARCHAR(20) NOT NULL,
      house_number VARCHAR(20) NOT NULL,              # because can be in shape like 256/22 thats why varchar 
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
      name varchar(30) not null
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

#script for table which represent bindings with book_title and library
make_user = '''
      CREATE TABLE User(
      user_id int AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(20) not null,
      surname VARCHAR(20) not null,
      email VARCHAR(30) not null,
      birth_date DATE not null,
      password VARCHAR(300),
      admin BOOLEAN,
      librarian BOOLEAN,
      distributor BOOLEAN,
      reader BOOLEAN,
      unregistered BOOLEAN,
      library_id int,
      CONSTRAINT fk_user foreign key (library_id) references Library(library_id)
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
      CONSTRAINT reservation_title foreign key (title_id) references Book_title(title_id),
      CONSTRAINT reservation_creator foreign key (creator_id) references User(user_id),
      CONSTRAINT reservation_handler foreign key (handler_id) references User(user_id)
      )
'''
insert_Book_title_author= '''INSERT INTO Book_title_author(time,until,title_id,creator_id,handler_id) 
                    VALUES(%s, %s,%s,%s,%s)
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
      CONSTRAINT lending_title foreign key (title_id) references Book_title(title_id),
      CONSTRAINT lending_creator foreign key (customer_id) references User(user_id),
      CONSTRAINT lending_handler foreign key (handler_id) references User(user_id)
      )
'''
insert_Book_title_author= '''INSERT INTO Book_title_author(time,until,title_id,creator_id,handler_id) 
                    VALUES(%s, %s,%s,%s,%s)
'''

make_votes = '''
      CREATE TABLE Votes(
      title_id int not null,
      library_id int not null,
      user_id int not null,
      yes boolean,
      no boolean,
      CONSTRAINT votes_title foreign key (title_id) references Book_title(title_id),
      CONSTRAINT votes_library foreign key (library_id) references Library(library_id),
      CONSTRAINT votes_user foreign key (user_id) references User(user_id),
      CONSTRAINT votes_user_library_title_unique UNIQUE (title_id, library_id, user_id)
      )
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
'''
'''
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

#how_many votes for book
#cursor.execute('''SELECT b.name,l.town, count(*)  FROM Book_title b JOIN Votes v ON b.title_id = v.title_id 
#               JOIN Library l ON l.library_id = v.library_id join User u on u.user_id = v.user_id GROUP BY l.town, b.name''')

#20 best books
#cursor.execute('''SELECT b.name,l.town, count(*)  FROM Book_title b JOIN Votes v ON b.title_id = v.title_id 
#               JOIN Library l ON l.library_id = v.library_id join User u on u.user_id = v.user_id GROUP BY l.town, b.name order by count(*) DESC limit 1''')

#cursor.execute('''ALTER TABLE Lending 
#ADD Column library_id int not null''')

#print(records)
#cursor.execute(make_library)
#cursor.execute(make_book_title)
#cursor.execute(make_book_title_library)
#cursor.execute(make_author)
#cursor.execute(make_book_title_author)
#cursor.execute(make_user)
#cursor.execute(make_votes)
##cursor.execute(make_lending)
#cursor.execute(make_reservation)

  
#to_insert = ("Jan","Baraniak","bar@tmp.sk",datetime.date(1978,5,1),"kdsada",int(False),int(False),int(False),int(True),int(False))
#cursor.execute('''INSERT INTO User(name, surname, email, birth_date, password, admin, librarian, distributor, reader, unregistered) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',to_insert)
#db_connection.commit()


#how many books on library

#autory
'''
library = "Mrazivé zlato"
parameter = tuple([library])
query = "SELECT a.name a.surname FROM  Book_title b JOIN Book_title_author ba ON b.title_id = ba.title_id 
              JOIN Author a ON ba.author_id = a.author_id WHERE b.name = %s"

cursor.execute(query,parameter)


x = tuple(["votes"])
#cursor.execute("ALTER TABLE Reservation DROP FOREIGN KEY lending_handler")

cursor.execute("ALTER TABLE Lending ADD CONSTRAINT lending_handler FOREIGN KEY (handler_id) references User(user_id) ON DELETE CASCADE")



cursor.execute("select * from user")
records = cursor.fetchall()
columns = [i[0] for i in cursor.description]

results = []
for row in records:
      results.append(dict(zip(columns, row)))  

print(results)

#param = tuple(["gorcak.damian@tmp.sk"])
query = "SELECT b.name, bl.count FROM Book_title b JOIN Book_title_library bl ON b.title_id = bl.title_id 
                    JOIN Library l ON bl.library_id = %s"

libraryid = 5
parameter = tuple([libraryid])
print(parameter)
cursor.execute(query,parameter)
records = cursor.fetchall()
columns = [i[0] for i in cursor.description]

results = []
for row in records:
      results.append(dict(zip(columns, row)))  

print(results)




print("Connected to:", db_connection.get_server_info())
db_connection.close()
cursor.close()
# enter your code here!

'''



#INSERT INTO `book_title_library` (`title_id`, `library_id`, `count`) VALUES ('235', '35', '2')#





####### boook title library inserting ##############

seed(1)

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
'''
######################### niesu v ziadnej kniznici #######################################################
query = "SELECT b.name FROM Book_title b where b.title_id not in (SELECT title_id from Book_title_library)"

libraryid = 5
#parameter = tuple([libraryid])
#print(parameter)
cursor.execute(query)
records = cursor.fetchall()
columns = [i[0] for i in cursor.description]

results = []
for row in records:
      results.append(dict(zip(columns, row)))  

print(results)
cursor.close()
'''
######book not in libraryies
#query = '''SELECT b.name FROM Book_title b where b.title_id not in (SELECT title_id from Book_title_library)
#                    '''

query = "ALTER TABLE Author RENAME COLUMN surname TO _surname"
libraryid = 5
#parameter = tuple([libraryid])
#print(parameter)
cursor.execute("select * from User")
records = cursor.fetchall()
columns = [i[0] for i in cursor.description]

results = []
for row in records:
      results.append(dict(zip(columns, row)))  

print(results)



print("Connected to:", db_connection.get_server_info())
db_connection.close()
cursor.close()