from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask_mysqldb import MySQL
from datetime import datetime
import random
import rds_db as db
import encrypt as enc
from werkzeug.utils import secure_filename
from collections import Counter
import os
import json
app = Flask(__name__)


app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'd0018e-1.c38ei448gz7c.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'Customer'
print("Password")
userpass = input()
app.config['MYSQL_PASSWORD'] = userpass
app.config['MYSQL_DB'] = 'D0018E1'

UPLOAD_FOLDER = 'C:/Users/Ellio/Desktop/D0018E/An-Internet-e-commerce-site-using-an-SQL-database/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)


@app.route('/')
@app.route('/index.html')
def index():
    try:
        if session['id']:
            1==1
    except:
        session['id'] = random.randrange(10000000,99999999)
    productTest = db.select_products(mysql)
    return render_template('index.html', productTest=productTest)

@app.route('/login')
# @app.route('/login.html')
def loginPage():
    return render_template('login.html')
@app.route('/l')
def reginPage():
    return render_template('create_user.html')


@app.route('/users')
def selectUsers():
    try:
        if session['isAdmin']:
            userDetails = db.select_all_users(mysql)
    # print(userDetails)
        for e in userDetails:
            print(e['customer_id'])
        return render_template('admin.html', userDetails=userDetails)
    except:
        var = "Access Denied"
        return render_template('index.html', var=var)


@app.route('/insert new customer',methods = ['post'])
def insert_new_user():
    if request.method == 'POST':
        email = request.form['email']
        if db.check_email(mysql, email):
            var = "Email in use"
            return render_template('index.html', var=var)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = enc.encrypPassword(request.form['password'])
        # password = request.form['password']
        date_of_birth = request.form['date_of_birth']
        db.insert_user(mysql,email,first_name,last_name,password, date_of_birth)
        account = db.get_user(mysql, email)
        db.update_shoppingCart(mysql, account['customer_id'], session['id'])
        session['loggedin'] = True
        session['id'] = account['customer_id']
        session['username'] = account['email']
        var = "User created"
        return render_template('index.html', var=var)
#TODO Implement what will happen when you loggin 
# Store the customer_id  
@app.route('/login',methods = ['post'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        # password = request.form['pwd']
        password = request.form['pwd']

        if email == "admin":
            app.config['MYSQL_USER'] = 'admin'
            app.config['MYSQL_PASSWORD'] = password
            var = "admin"
            session['loggedin'] = True
            session['isAdmin'] = True
            return render_template('admin.html', var=var)

        if db.check_credentails(mysql,email, password):
            account = db.get_user(mysql,email)

            # cursor = conn.cursor()
            # cursor.execute('SELECT * FROM accounts WHERE email = % s', (email))
            if account:
                # print("account", account)
                session['loggedin'] = True
                session['id'] = account['customer_id']
                session['username'] = account['email']
                # print("acount", account['customer_id'])
            
            var = session['id']

            return redirect('/')
    var = "Account error"
    return render_template('index.html', var=var)

@app.route('/logout')
def logout():
    try:
        if session['isAdmin']:
            app.config['MYSQL_USER'] = 'Customer'
            app.config['MYSQL_PASSWORD'] = userpass
            session.pop('isAdmin', False)
    except:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
    return redirect('/')

@app.route('/Addproduct', methods=['POST', 'GET'])
def Addproduct():
    if request.method == 'GET':
        # if session['isAdmin']:
        #         products = db.select_products(mysql)
        # return render_template('admin.html', products=products)
        try:
            if session['isAdmin']:
                products = db.select_products(mysql)
            return render_template('admin.html', products=products)
        except:
            var = "Access Denied"
            return render_template('index.html', var=var)
    elif request.method == 'POST':
        # try:
            if session['isAdmin']:
                product_name = request.form['product_name']
                price = request.form['price']
                stock = request.form['stock']
               
                file = request.files['img1']
                filename = secure_filename(file.filename)
                image_address1 = "images/" + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if int(stock) > 0:
                    last_restock_date = datetime.now()
                else:
                    last_restock_date = None
                db.insert_product(mysql, product_name, price, stock, last_restock_date, image_address1)
                var = "product created"
            return render_template('admin.html', var=var)
        # except:
        #     var = "Access Denied"
        #     return render_template('index.html', var=var)


@app.route('/edit_product', methods=['POST','GET'])
def editProduct():
    if request.method == 'GET':
        # try:
        # if session['isAdmin']:
        product_id = request.args['product_id']
        print("PRODUCT_ID", product_id)
        product = db.get_product(mysql, product_id)
        print("PRODUCT", product)
        return render_template('edit_product.html', product=product, product_id=product_id)
        # except:
        #     var = "Access Denied"
        #     return render_template('index.html', var=var)
    elif request.method == 'POST':
        # try:
            if session['isAdmin']:
                product_id = request.form['product_id']
                product = db.get_product(mysql, product_id)
                
                product_name = request.form['product_name']
                if product_name == '' or product_name is None:
                    product_name = product['product_name']
                
                price = request.form['price']
                if price == "" or price is None:
                    price = 0
                if int(price) <= 0:
                    price = product['product_price']  

                stock = request.form['stock']
                if stock == "" or stock is None:
                    stock = 0

                if int(stock) <= 0 :
                    stock = product['product_available_amount']
                    last_restock_date = product['last_restock_date']
                    totalStock = product['product_total_amount']
                else:
                    totalStock = int(stock) + product['product_total_amount']
                    stock = int(stock) + product['product_available_amount']
                    last_restock_date = datetime.now()

                db.update_product(mysql, product_id, product_name, price, stock, last_restock_date, totalStock)
                var = "changed"
            return render_template('admin.html', var=var)
    
    
@app.route('/checkout')
def checkOut():
    try:
        if session['loggedin']:
            customerId = session['id']
            sessionID = None
    except:
        return redirect('/l')
    
    orderID = db.insert_order(mysql, customerId, datetime.now())
    cart = db.get_shoppingCart(mysql, customerId, sessionID)
    totalPrice = 0
#-------------- Insert product updated info ------------------------- #
    for item in cart:
        products = db.get_product(mysql,item['product_id'])
        item['price'] = products['product_price']
        item['product_name'] = products['product_name']
        item['TotalPrice'] = int(item['price']) * int(item['quantity'])
        totalPrice = totalPrice + item['TotalPrice']
        db.insert_orderProduct(mysql, customerId, orderID, item['product_id'], item['product_name'], item['price'], item['quantity'], item['TotalPrice'])
    db.update_order(mysql, orderID, totalPrice)

    checkOut = db.get_product_from_order(mysql, orderID)
    
    return render_template('order_conf.html',checkOut=checkOut,order_product_id = orderID)

# @app.route('/shoppingcart', methods=['POST'])
# def shoppingcart():
#     cart_array_cookie = json.loads(request.cookies.get('cartArray'))
#     cart_array_cookie_nodup = list(dict.fromkeys(cart_array_cookie))
#     occurrences = Counter(cart_array_cookie)
#     shoppingcart = []
#     for product_id in cart_array_cookie_nodup:
#         product = db.get_product(mysql, product_id)
#         product["amount"] = int(occurrences[str(product_id)])
#         product["total_price"]  = int(product["amount"])*int(product['product_price'])
#         shoppingcart.append(product)
#     return jsonify(shoppingcart)

#     return render_template('shopping_cart.html',shoppingcart=shoppingcart)

# @app.route('/add-to-cart', methods=['POST'])
# def add_product_to_cart():
#     productId = request.form.get('product_id')
#     productInCart = db.get_product_in_cart(mysql, productId)
#     if productInCart is None:
#         productInfo = db.get_product(mysql, productId)
#         db.insert_shoppingCart(mysql, customer_id, )

#     db.insert_shoppingCart

@app.route('/add-to-cart', methods=['POST'])
def addToShoppingCart():
    productId = request.form['product_id']
    amount = request.form['quantity']
    print("hej")

    try:
        if session['loggedin']:
            customerId = session['id']
            sessionID = None
    except:
        customerId = None
        sessionID = session['id']
    print("Customer ID     " ,customerId)
    print("Session ID      " ,sessionID)
    print("product ID", productId)
    productInCart = db.get_shoppingCartItem(mysql, customerId, sessionID, productId)
    print(productInCart)
    if productInCart:
        print("har produkt")
        quantity = productInCart ['quantity'] + int(amount)
        db.update_shoppingCartItem(mysql, customerId, sessionID, productId,quantity,datetime.now())
    else:
        print("har inte  produkt")
        quantity = amount
        db.insert_shoppingCart(mysql, customerId, sessionID, productId,quantity,datetime.now())
    return redirect('/')

@app.route('/shopping_cart.html')
def cartPage():
    try:
        if session['loggedin']:
            customerId = session['id']
            sessionID = None
    except:
        customerId = None
        sessionID = session['id']
    cartItems = db.get_shoppingCart(mysql, customerId, sessionID)
    for item in cartItems:
        print(item)
        products = db.get_product(mysql,item['product_id'])
        item['price'] = products['product_price']
        item['product_name'] = products['product_name']
        item['TotalPrice'] = int(item['price']) * int(item['quantity'])

        
    return render_template('shopping_cart.html', cartItems = cartItems)


if __name__ == "__main__":
    app.run(port=5002, debug=True)


@app.route('/review', methods=['POST'])
def addReview():
    return