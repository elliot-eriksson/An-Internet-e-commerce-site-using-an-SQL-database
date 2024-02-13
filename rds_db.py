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

def get_product(mysql,product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Products WHERE product_id = % s', (product_id,))
    product = cur.fetchone()
    return product

def get_product_in_cart(mysql, product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Cart WHERE product_id = % s', (product_id,))
    product = cur.fetchone()
    return product

def get_product_from_order(mysql, order_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM OrderProducts WHERE order_id = % s', (order_id,))
    products = cur.fetchall()
    return products

def get_user(mysql,email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users WHERE email = % s', (email,))
    user = cur.fetchone()
    return user

def get_shoppingCart(mysql,customer_id,session_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if customer_id is None:
        cur.execute('SELECT * FROM Cart WHERE session_id = % s', (session_id,))
    else:
        cur.execute('SELECT * FROM Cart WHERE customer_id = % s', (customer_id,))
    cart = cur.fetchall()
    return cart

def get_shoppingCartItem(mysql, customer_id, session_id, product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if customer_id is None:
        cur.execute('SELECT * FROM Cart WHERE session_id = %s and product_id = %s', (session_id,product_id,))
    else:
        cur.execute('SELECT * FROM Cart WHERE customer_id = %s and product_id = %s', (session_id,product_id,))
    item = cur.fetchone()
    return item


def insert_product(mysql, product_name, price, stock, last_restock_date, image_address1):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Products (product_name, product_price, product_available_amount, product_total_amount, last_restock_date, image_address1) VALUES (%s,%s,%s,%s,%s,%s)"
        ,(product_name, price, stock, stock, last_restock_date, image_address1,))
    mysql.connection.commit()

def insert_user(mysql,email, first_name, last_name, password, date_of_birth):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Users (email, first_name, last_name, password, date_of_birth) VALUES (%s,%s,%s,%s,%s)"
        ,(email, first_name, last_name, password, date_of_birth,))
    mysql.connection.commit()

def insert_order(mysql, customer_id, date_of_purchase):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Orders (customer_id, date_of_purchase, total_price) VALUES (%s,%s,%s)"
        ,(customer_id, date_of_purchase, 0,))
    mysql.connection.commit()
    return cur.execute('select last_insert_id() from Orders')

def insert_shoppingCart(mysql, customer_id, session_id, product_id, price, product_amount, createdAt, updatedAt):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Cart (customer_id, session_id, product_id, price, quantity, createdAt, updatedAt) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        ,(customer_id, session_id, product_id, price, product_amount, createdAt, updatedAt,))
    mysql.connection.commit()

def insert_orderProduct(mysql,customer_id, order_id, product_id, product_name, product_price, amount, total_price):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO OrderProducts (customer_id, order_id, product_id, product_name, product_price, amount, total_price) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        ,(customer_id,order_id, product_id, product_name, product_price, amount, total_price,))
    mysql.connection.commit()


def update_order(mysql, order_id, total_price):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("UPDATE Orders SET total_price =%s Where order_id= %s", (total_price, order_id,))
    mysql.connection.commit()


def update_product(mysql, product_id, product_name, price, stock, last_restock_date, totalStock):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("UPDATE Products SET product_name = %s, product_price = %s, product_available_amount = %s, product_total_amount = %s, last_restock_date = %s WHERE product_id = %s "
        ,(product_name, price, stock, totalStock, last_restock_date, product_id,))
    mysql.connection.commit()

def update_shoppingCartItem(mysql, customer_id, session_id, product_id, quantity, updatedAt,price):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if customer_id is None:
        cur.execute('UPDATE Cart SET quantity = %s, updatedAt = %s, price =%s WHERE session_id = %s and product_id = %s', (quantity, updatedAt,price,session_id,product_id,))
    else:
        cur.execute('UPDATE Cart SET quantity = %s, updatedAt = %s, price =%s WHERE customer_id = %s and product_id = %s', (quantity, updatedAt,price,customer_id,product_id,))
    mysql.connection.commit()

def delete_shoppingCartItem(mysql, customer_id, session_id, product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if customer_id is None:
        cur.execute ('DELETE FROM Cart WHERE session_id = %s and product_id = %s', (session_id, product_id,))
    else:
        cur.execute ('DELETE FROM Cart WHERE customer_id = %s and product_id = %s', (customer_id, product_id,))
    mysql.connection.commit()

def delete_shoppingCart(mysql, customer_id, session_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if customer_id is None:
        cur.execute ('DELETE FROM Cart WHERE session_id = %s', (session_id,))
    else:
        cur.execute ('DELETE FROM Cart WHERE customer_id = %s', (customer_id,))
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

