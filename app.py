from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask_mysqldb import MySQL
from datetime import datetime
import rds_db as db
import encrypt as enc
from form import AddProducts
from werkzeug.utils import secure_filename
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

            return render_template('index.html', var=var)
    var = "Account error"
    return render_template('index.html', var=var)

@app.route('/logout')
def logout():
    if session['isAdmin']:
        app.config['MYSQL_USER'] = 'Customer'
        app.config['MYSQL_PASSWORD'] = userpass
        session.pop('isAdmin', False)
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

@app.route('/Add to cart', methods=['POST'])
def addToCart():
    var = "product Added"
    productTest = db.select_products(mysql)
    return render_template('index.html', productTest=productTest, var=var)

@app.route('/edit_product', methods=['GET'])
def editProduct():
    if request.method == 'GET':
        # try:
        # if session['isAdmin']:
        product_id = request.form['product_id']
        products = db.get_product(mysql, product_id)
        return render_template('edit_product.html', products=products, product_id=product_id)
        # except:
        #     var = "Access Denied"
        #     return render_template('index.html', var=var)
    elif request.method == 'POST':
        # try:
            if session['isAdmin']:
                product_id = request.form['product_id']
                product = db.get_product(mysql, product_id)
                product_name = request.form['product_name']
                if product_name == '':
                    product_name = product['product_name']
                price = request.form['price']
                if price == '' or int(price) <= 0:
                    price = product['price']  
                stock = request.form['stock']
                if int(stock) > 0:
                    last_restock_date = datetime.now()
                else:
                    last_restock_date = None
                if stock == "" or int(stock) == 0:
                    stock = product['product_available_amount']
                    last_restock_date = product['last_restock_date']
                elif int(stock) < 0:
                    var = "Cant enter negative amount of stock"
                    return render_template('admin.html', var=var)
                else:
                    stock = int(stock) + product['product_available_amount']
                    totalStock = int(stock) + product['product_total_amount']


                db.update_product(mysql, product_id, price, stock, last_restock_date, totalStock)
                var = "changed"
            return render_template('admin.html', var=var)
    
@app.route('/checkout')
def checkOut():
    cart_array_cookie = json.loads(request.cookies.get('cartArray'))
    print("---------------",cart_array_cookie)
    # Parse the JSON string to get the cartArray

    # You can now use 'cart_array' in your template or logic
    return render_template('index.html', var=cart_array_cookie)
    
    
if __name__ == "__main__":
    app.run(port=5002, debug=True)
