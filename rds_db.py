import encrypt as enc
import MySQLdb.cursors

def select_all(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users')
    test = cur.fetchall()
    return test


def get_user(mysql,email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users WHERE email = % s', (email,))
    test = cur.fetchone()
    return test
        

def insert_user(mysql,email, first_name, last_name, password, date_of_birth):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Users (email, first_name, last_name, password, date_of_birth) VALUES (%s,%s,%s,%s,%s)"
        ,(email, first_name, last_name, password, date_of_birth,))
    cur.commit()

    
def check_email(mysql,email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT count(email) FROM Users WHERE email= %s", (email,))
    details = cur.fetchall()
    for elem in str(details):
        if elem == "0":
            return False
    return True
    
def check_credentails(mysql, email, password):
    if (get_user(mysql, email)) == 0:
        print("missing user")
        return False
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT password FROM Users WHERE email= %s", (email,))
    checkPass = cur.fetchall()
    # print("element", checkPass['password'])
    for element in checkPass:
        currentPass = element['password']
    return enc.decryptPassword(password, currentPass)