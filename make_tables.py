import mysql.connector as mysql


# enter your server IP address/domain name
HOST = "sql11.freesqldatabase.com" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "sql11449509"
# this is the user you create
USER = "sql11449509"
# user password
PASSWORD = "1JR1eSrwxJ"
# connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
cursor = db_connection.cursor()


#Creating table as per requirement

sql ='''CREATE TABLE tmp(
   id int NOT NULL,
   AGE INT,
   SEX CHAR(1),
   PRIMARY KEY (id)
)'''

sql2 ='''CREATE TABLE tmp2(
   id int NOT NULL,
   sex INT,
   tmpid int,
   PRIMARY KEY (id),
   FOREIGN KEY (tmpid) REFERENCES tmp(id)
)'''

sql = '''INSERT INTO tmp(id,AGE,SEX) 
   VALUES (2,21,"M") 
'''
sql2 = '''INSERT INTO tmp2(id,sex,tmpid) 
   VALUES (2,22,2) 
'''

sql = '''select *
from tmp2 u join tmp s on u.id = s.id and u.id = 2;
'''


cursor.execute(sql)



records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)

print(records)
print("Connected to:", db_connection.get_server_info())

db_connection.close()
cursor.close()
# enter your code here!