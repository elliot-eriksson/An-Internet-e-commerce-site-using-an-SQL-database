import encrypt as enc
import MySQLdb.cursors

def select_all_users(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users')
    users = cur.fetchall()
    return users

def select_products(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Products')
    products = cur.fetchall()
    return products

def get_product(mysql,product_name):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Products WHERE product_name = % s', (product_name,))
    product = cur.fetchone()
    return product

def insert_product(mysql, product_name, price, stock, last_restock_date, image_address1):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Products (product_name, product_price, product_available_amount, product_total_amount, last_restock_date, image_address1) VALUES (%s,%s,%s,%s,%s,%s)"
        ,(product_name, price, stock, stock, last_restock_date, image_address1,))
    mysql.connection.commit()

def get_user(mysql,email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users WHERE email = % s', (email,))
    user = cur.fetchone()
    return user
        

def insert_user(mysql,email, first_name, last_name, password, date_of_birth):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Users (email, first_name, last_name, password, date_of_birth) VALUES (%s,%s,%s,%s,%s)"
        ,(email, first_name, last_name, password, date_of_birth,))
    mysql.connection.commit()


    
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

