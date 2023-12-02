import mysql.connector
from mysql.connector import Error

def create_con(hostname, username, userpw, dbname):
    connection  = None
    try:
        connection  = mysql.connector.connect(
            host = hostname,
            user = username,
            password = userpw,
            database = dbname
        )
        print("success")
    except Error as e:
        print(f'the error {e} occured')
    return connection

conn = create_con('test1.cvnfv4bycwvt.us-east-2.rds.amazonaws.com', 'admin', 'admin111', 'test1db')
cursor = conn.cursor(dictionary = True)
sql = 'select * from users'
cursor.execute(sql)
rows = cursor.fetchall()

for user in rows:
    print(user)
    print('first name is: ' + user['firstname'])

