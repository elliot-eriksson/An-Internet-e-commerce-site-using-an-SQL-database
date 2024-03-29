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

def select_rating(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Rating')
    ratings = cur.fetchall()
    return ratings


def get_product(mysql,product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Products WHERE product_id = % s', (product_id,))
    product = cur.fetchone()
    return product

def get_order(mysql,order_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Orders WHERE order_id = % s', (order_id,))
    order = cur.fetchone()
    return order

def get_product_in_cart(mysql, product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Cart WHERE product_id = % s', (product_id,))
    product = cur.fetchone()
    return product

def get_all_product_from_order(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM OrderProducts WHERE conf IS NULL')
    products = cur.fetchall()
    return products

def get_a_product_from_order(mysql,order_product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM OrderProducts WHERE order_product_id = %s', (order_product_id,))
    products = cur.fetchone()
    return products

def get_product_available_amount(mysql,product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT product_available_amount FROM Products WHERE product_id = % s', (product_id,))
    product = cur.fetchone()
    return product


def get_confirm_orderProducts(mysql, order_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM OrderProducts WHERE order_id = % s', (order_id,))
    products = cur.fetchall()
    return products

def get_product_from_customerorder(mysql, product_id,customer_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM OrderProducts WHERE customer_id = % s and product_id = %s ORDER BY order_product_id DESC', (customer_id, product_id,))
    product = cur.fetchone()
    return product

def get_user(mysql,email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users WHERE email = % s', (email,))
    user = cur.fetchone()
    return user

def get_rating(mysql,customer_id, product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Rating WHERE customer_id = %s and  product_id = %s', (customer_id,product_id))
    rating = cur.fetchone()
    return rating

def get_user_name(mysql,customer_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT first_name FROM Users WHERE customer_id = % s', (customer_id,))
    user = cur.fetchone()
    return user

def get_review(mysql,product_id, parent_id):
    if parent_id == 0:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM Reviews WHERE product_id = %s and parent_id IS NULL', (product_id, ))
        review = cur.fetchall()
        return review
    elif parent_id == 1:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM Reviews WHERE product_id = %s and parent_id IS NOT NULL', (product_id, ))
        review = cur.fetchall()
        return review
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM Reviews WHERE product_id = %s and parent_id =%s ', (product_id, parent_id))
        review = cur.fetchall()
        return review


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
        cur.execute('SELECT * FROM Cart WHERE customer_id = %s and product_id = %s', (customer_id,product_id,))
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
    cur.execute('select max(order_id) as OrderID from Orders where customer_id = %s ', (customer_id,))
    item = cur.fetchone()
    return item

def insert_shoppingCart(mysql, customer_id, session_id, product_id, product_amount, updatedAt):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Cart (customer_id, session_id, product_id, quantity, updatedAt) VALUES (%s,%s,%s,%s,%s)"
        ,(customer_id, session_id, product_id, product_amount, updatedAt,))
    mysql.connection.commit()

def insert_orderProduct(mysql,customer_id, order_id, product_id, product_name, product_price, amount, total_price):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO OrderProducts (customer_id, order_id, product_id, product_name, product_price, amount, total_price) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        ,(customer_id,order_id, product_id, product_name, product_price, amount, total_price,))
    mysql.connection.commit()

def insert_review(mysql, product_id, customer_id, parent_id, publishedAt, purchase_date, review, name):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Reviews (product_id, customer_id, parent_id, publishedAt, purchase_date, review, name) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        ,(product_id,customer_id, parent_id, publishedAt, purchase_date, review, name,))
    mysql.connection.commit()

def insert_rating(mysql, customer_id, product_id, rating):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Rating (customer_id, product_id, rating) VALUES (%s,%s,%s)"
        ,(customer_id, product_id, rating,))
    mysql.connection.commit()


def update_rating(mysql,customer_id, product_id, rating):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("UPDATE Rating SET rating =%s Where customer_id= %s and product_id = %s ", (rating, customer_id,product_id,))
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

def update_products_from_order(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('UPDATE OrderProducts SET conf = true WHERE conf IS NULL')
    mysql.connection.commit()

def update_available_amount(mysql,product_available_amount, product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('UPDATE Products SET product_available_amount = %s WHERE product_id = %s '
        ,( product_available_amount, product_id,))
    mysql.connection.commit()

def update_a_product_from_order(mysql, order_product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('UPDATE OrderProducts SET conf = true WHERE order_product_id = %s', (order_product_id,))
    mysql.connection.commit()

def update_shoppingCartItem(mysql, customer_id, session_id, product_id, quantity, updatedAt):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if customer_id is None:
        cur.execute('UPDATE Cart SET quantity = %s, updatedAt = %sWHERE session_id = %s and product_id = %s', (quantity, updatedAt,session_id,product_id,))
    else:
        cur.execute('UPDATE Cart SET quantity = %s, updatedAt = %sWHERE customer_id = %s and product_id = %s', (quantity, updatedAt,customer_id,product_id,))
    mysql.connection.commit()

def update_shoppingCart(mysql, customer_id, session_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('UPDATE Cart SET session_id = NULL, customer_id = %s WHERE session_id = %s', (customer_id, session_id,))
    mysql.connection.commit()

def update_productAvrageRating(mysql, product_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('UPDATE Products SET avrage_rating = (SELECT AVG(rating) FROM Rating where product_id = %s) WHERE product_id = %s', (product_id, product_id,))
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

