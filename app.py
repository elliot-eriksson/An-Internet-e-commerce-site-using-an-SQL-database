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

    try:
        if session['loggedin']:
            customerId = session['id']
            sessionId = None
    except:
        customerId = None
        sessionId = session['id']

    productTest = db.select_products(mysql)
    cartItems = db.get_shoppingCart(mysql, customerId, sessionId)
    totalPrice = 0
    for item in cartItems:
        products = db.get_product(mysql,item['product_id'])
        item['price'] = products['product_price']
        item['product_name'] = products['product_name']
        item['TotalPrice'] = int(item['price']) * int(item['quantity'])
        totalPrice = totalPrice + item['TotalPrice']
    print(cartItems)
    return render_template('index.html', productTest=productTest, cartItems = cartItems)

@app.route('/login')
# @app.route('/login.html')
def loginPage():
    try:
        if session["loggedin"]:
            var = "already logged in"
            return render_template("login.html",var = var)
    except:
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
            return redirect('/')
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
        return redirect('/')
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
        try:    
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
        except:
            return redirect("/")
            
    return redirect('/')

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

@app.route('/show-orders')
def showOrders():
    orders = db.get_all_product_from_order(mysql)
    return render_template('admin.html', orders=orders)

@app.route('/confirm-a-order', methods=['POST'])
def confirmAOrder():
    orderProductId = request.form['orderproductid']
    # orderProductId = request.args['orderproductid']
    print("---------------------------",orderProductId)
    order = db.get_a_product_from_order(mysql, orderProductId)
    amountPurchased = order['amount']
    amountBefore = db.get_product_available_amount(mysql, order["product_id"] )
    if amountPurchased > amountBefore['product_available_amount']:
        var = "Not enough of " + order["product_name"] + " in stock"  
        return render_template('admin.html', var=var)
    quantity = amountBefore['product_available_amount'] - amountPurchased 
    db.update_available_amount(mysql, quantity, order["product_id"] )

    db.update_a_product_from_order(mysql, orderProductId)
    return render_template('admin.html')
    
@app.route('/confirm-orders')
def confirmOrder():
    orders = db.get_all_product_from_order(mysql)
    
    for order in orders:
        productId = order['product_id']
        amountPurchased = order['amount']
        amountBefore = db.get_product_available_amount(mysql, productId)
        if amountPurchased > amountBefore['product_available_amount']:
            var = "Not enough of " + order["product_name"] + " in stock manually confirm orders"  
            return render_template('admin.html', var=var)
        quantity = amountBefore['product_available_amount'] - amountPurchased 
        db.update_available_amount(mysql, quantity, productId )
        db.update_a_product_from_order(mysql, order["order_product_id"])

    return render_template('admin.html')
    
@app.route('/checkout')
def checkOut():
    try:
        if session['loggedin']:
            customerId = session['id']
            sessionID = None
    except:
        return redirect('/l')
    
    order = db.insert_order(mysql, customerId, datetime.now())
    orderID = order['OrderID']
    cart = db.get_shoppingCart(mysql, customerId, sessionID)
    totalUnitPrice = 0
#-------------- Insert product updated info ------------------------- #
    for item in cart:
        products = db.get_product(mysql,item['product_id'])
        item['price'] = products['product_price']
        item['product_name'] = products['product_name']
        item['totalUnitPrice'] = int(item['price']) * int(item['quantity'])
        totalUnitPrice = totalUnitPrice + item['totalUnitPrice']
        print("CustomerID", customerId)
        print("ORDER ID", orderID)
        print("ORDER ID", item['product_id'])
        
        db.insert_orderProduct(mysql, customerId, orderID, item['product_id'], item['product_name'], item['price'], item['quantity'], item['totalUnitPrice'])
    db.update_order(mysql, orderID, totalUnitPrice)

    checkOut = db.get_confirm_orderProducts(mysql, orderID)
    
    db.delete_shoppingCart(mysql, customerId, sessionID)
    
    return render_template('order_conf.html',checkOut=checkOut,order_product_id = orderID, totalUnitPrice = totalUnitPrice)

@app.route('/add-to-cart', methods=['POST'])
def addToShoppingCart():
    productId = request.form['product_id']
    amount = request.form['quantity']
    try:
        if session['loggedin']:
            customerId = session['id']
            sessionID = None
    except:
        customerId = None
        sessionID = session['id']
    product = db.get_product(mysql, productId)

    if not isinstance(amount, int):
        var = "Amount of product needs to be a number"
        productTest = db.select_products(mysql)
        cartItems = db.get_shoppingCart(mysql, customerId, session['id'])
        for item in cartItems:
            products = db.get_product(mysql,item['product_id'])
            item['price'] = products['product_price']
            item['product_name'] = products['product_name']
            item['TotalPrice'] = int(item['price']) * int(item['quantity'])
            totalPrice = totalPrice + item['TotalPrice']
        return render_template('index.html', productTest=productTest, cartItems = cartItems, var=var)
    elif int(amount) <= 0:
        var = "Amount of product needs to greater than 0"
        productTest = db.select_products(mysql)
        cartItems = db.get_shoppingCart(mysql, customerId, session['id'])
        for item in cartItems:
            products = db.get_product(mysql,item['product_id'])
            item['price'] = products['product_price']
            item['product_name'] = products['product_name']
            item['TotalPrice'] = int(item['price']) * int(item['quantity'])
            totalPrice = totalPrice + item['TotalPrice']
        return render_template('index.html', productTest=productTest, cartItems = cartItems, var=var)


    productInCart = db.get_shoppingCartItem(mysql, customerId, sessionID, productId)
    print(productInCart)
    if productInCart:
        print("har produkt")
        quantity = productInCart ['quantity'] + int(amount)
        if product["product_available_amount"] < int(quantity):
            var = "To many"+ product["product_name"] +" chosen max available: " + str(product["product_available_amount"])
            productTest = db.select_products(mysql)
            cartItems = db.get_shoppingCart(mysql, customerId, session['id'])
            for item in cartItems:
                products = db.get_product(mysql,item['product_id'])
                item['price'] = products['product_price']
                item['product_name'] = products['product_name']
                item['TotalPrice'] = int(item['price']) * int(item['quantity'])
                totalPrice = totalPrice + item['TotalPrice']
            return render_template('index.html', productTest=productTest, cartItems = cartItems, var=var)
        db.update_shoppingCartItem(mysql, customerId, sessionID, productId,quantity,datetime.now())
    else:
        print("har inte  produkt")
        quantity = amount
        if product["product_available_amount"] < int(quantity):
            var = "To many"+ product["product_name"] +" chosen max available: " + str(product["product_available_amount"])
            productTest = db.select_products(mysql)
            cartItems = db.get_shoppingCart(mysql, customerId, session['id'])
            for item in cartItems:
                products = db.get_product(mysql,item['product_id'])
                item['price'] = products['product_price']
                item['product_name'] = products['product_name']
                item['TotalPrice'] = int(item['price']) * int(item['quantity'])
                totalPrice = totalPrice + item['TotalPrice']
            return render_template('index.html', productTest=productTest, cartItems = cartItems, var=var)
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

# ------------------- view product and reviews ----------------------------
@app.route('/view-product', methods=['GET'])
def viewProduct():
    
    productId = request.args['product_id']
    product = db.get_product(mysql, productId)
    
    topreview = db.get_review(mysql, productId, 0)
    answers = db.get_review(mysql, productId, 1)

    ratings = db.select_rating(mysql)

    return render_template('productpage.html', product = product, topreview = topreview, answers = answers, ratings = ratings)

@app.route('/review', methods=['POST'])
def addReview():
    productId = request.form['product_id']
    # try:
    product = db.get_product_from_customerorder(mysql, productId, session['id'])
    if session['loggedin'] and product:
        order = db.get_order(mysql, product["order_id"])
        customer_id = session['id']
        customer  = db.get_user_name(mysql, customer_id)
        name = customer["first_name"]
        parent_id = None
        publishedAt = datetime.now()
        purchase_date = order["date_of_purchase"]
        review = request.form['review']
        db.insert_review(mysql, productId, customer_id, parent_id, publishedAt, purchase_date, review, name)
        rating = request.form.get('starRating')
        if db.get_rating(mysql, customer_id, productId):
            db.update_rating(mysql, customer_id, productId, rating)
        else:
            db.insert_rating(mysql, customer_id, productId, rating)
        db.update_productAvrageRating(mysql, productId)
    else:
        var = "<h1>Needs to have purchase product to add review</h1>"
        return var 
    product = db.get_product(mysql, productId)
    topreview = db.get_review(mysql, productId, 0)
    answers = db.get_review(mysql, productId, 1)
    ratings = db.select_rating(mysql)

    return render_template('productpage.html', product = product, topreview = topreview, answers = answers, ratings = ratings)
    # except: 
    #     var = "Needs to have acount to add review"
    #     return "<h1>Needs to have purchase product to add review</h1>"
    
@app.route('/rating', methods=['POST'])
def addRating():
    productId = request.form['product_id']
    try:
        product = db.get_product_from_customerorder(mysql, productId, session['id'])
        if session['loggedin'] and product:
            customer_id = session['id']
            rating = request.form['rating']
            if db.get_rating(mysql, customer_id, productId):
                db.update_rating(mysql, customer_id, productId, rating)
            else:
                db.insert_rating(mysql, customer_id, productId, rating)
            db.update_productAvrageRating(mysql, productId)
        else:
            var = "<h1>Needs to have purchase product to add rating</h1>"
            return var 
        product = db.get_product(mysql, productId)
        topreview = db.get_review(mysql, productId, 0)
        answers = db.get_review(mysql, productId, 1)
        ratings = db.select_rating(mysql)

        return render_template('productpage.html', product = product, topreview = topreview, answers = answers, ratings = ratings)
    except: 
        var = "Needs to have acount to add review"
        return "<h1>Needs to have purchase product to add rating</h1>"
    



@app.route('/reviewAns', methods=['POST'])
def addAnswer():
    productId = request.form['product_id']
    parent_id = request.form['parent_id']
    try:
        product = db.get_product_from_customerorder(mysql, productId, session['id'])
        if session['loggedin'] and product:
            order = db.get_order(mysql, product["order_id"])
            customer_id = session['id']
            publishedAt = datetime.now()
            purchase_date = order["date_of_purchase"]
            customer  = db.get_user_name(mysql, customer_id)
            name = customer["first_name"]
            review = request.form['review']
            db.insert_review(mysql, productId, customer_id, parent_id, publishedAt, purchase_date, review,name)
        elif session['isAdmin']:
            customer_id = None
            publishedAt = datetime.now()
            purchase_date = None
            name = "Admin"
            review = request.form['review']
            db.insert_review(mysql, productId, customer_id, parent_id, publishedAt, purchase_date, review, name)
        product = db.get_product(mysql, productId)
        topreview = db.get_review(mysql, productId, 0)
        answers = db.get_review(mysql, productId, 1)
        ratings = db.select_rating(mysql)

        return render_template('productpage.html', product = product, topreview = topreview, answers = answers, ratings = ratings)
    except:
        try: 
            if session['loggedin']:
                var = "Needs to have purchase product to add review"
                return redirect('/login', var=var) 
        except:    
            var = "Needs to have acount to add review"
            return redirect('/login', var=var)

@app.route('/remove-item-from-cart', methods=['POST'])       
def removeProductInCart():
    print("Enter")
    try:
        if session['loggedin']:
            customerId = session['id']
            sessionId = None
    except:
        customerId = None
        sessionId = session['id']
    print("customerId", customerId)
    print("sessionId", sessionId)


    productId = request.form['product_id']
    print("product_id", productId)
    db.delete_shoppingCartItem(mysql,customerId,sessionId, productId)
    totalPrice = 0
    cartItems = db.get_shoppingCart(mysql, customerId, sessionId)
    for item in cartItems:
        products = db.get_product(mysql,item['product_id'])
        item['price'] = products['product_price']
        item['product_name'] = products['product_name']
        item['TotalPrice'] = int(item['price']) * int(item['quantity'])
        totalPrice = totalPrice + item['TotalPrice']
       
    return redirect('/index.html')

@app.route('/clear-cart', methods=['POST'])       
def clearCart():
    try:
        if session['loggedin']:
            customerId = session['id']
            sessionId = None
    except:
        customerId = None
        sessionId = session['id']
    db.delete_shoppingCart(mysql, customerId, sessionId)
    return redirect("/index.html")


if __name__ == "__main__":
    app.run(port=5002, debug=True)


