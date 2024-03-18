from flask import render_template, redirect, url_for, flash, request, session
from app import app, db, login_manager
from app.forms.user import UserRegistrationForm, UserLoginForm
from app.models.user import User, Userorder
from flask_login import login_required, current_user, logout_user, login_user
import secrets
from collections import defaultdict



@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        # Extract data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        country = form.country.data
        state = form.state.data
        city = form.city.data
        address = form.address.data
    
        # Check if the email or username already exists
        existing_user_email = User.query.filter_by(email=email).first()
        existing_user_username = User.query.filter_by(username=username).first()

        if existing_user_email:
            flash('Email already exists. Please use a different email.', 'error')
        elif existing_user_username:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            # Create a new User object
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                country=country,
                state=state,
                city=city,
                address=address
            )
            new_user.set_password(password)

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('user_login'))

    return render_template('root/register.html', form=form, title="User Registration")




@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    if form.validate_on_submit():
        email_or_username = form.email_or_username.data
        password = form.password.data

        
        user = User.query.filter_by(email=email_or_username).first() or User.query.filter_by(username=email_or_username).first()
        print(user)  # Add this line to check the value of user
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome {email_or_username}. You are logged in now', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email/username or password combination.', 'danger')
            return redirect(url_for(user_login))

    return render_template('root/login.html', form=form, title="User Login")




@app.route('/user/logout', methods=['POST'])
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        
        # Calculate total amount and quantities of each item
        total_amount = 0
        quantities = defaultdict(int)
        for key, product in session['Shoppingcart'].items():
            total_amount += product['price'] * product['quantity']
            quantities[key] += product['quantity']

        try:
            # Create Userorder instance with updated orders
            order = Userorder(invoice=invoice, customer_id=customer_id,
                              orders=session['Shoppingcart'], total_amount=total_amount, quantities=quantities)
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash("Your order has been sent", "success")
            return redirect(url_for('orders', invoice=invoice))
        
        except Exception as e:
            print(e)
            flash('Something went wrong while submitting order', 'danger')
            return redirect(url_for('getCart'))
        

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        customer_id = current_user.id 
        customer = User.query.filter_by(id=customer_id).first()
        orders = Userorder.query.filter_by(customer_id=customer_id).all()
    
    else:
        return redirect(url_for('user_login'))
    return render_template('root/ordertrack.html', invoice = invoice, customer = customer, orders=orders)

@app.route('/order_details/<invoice>')
@login_required
def order_details(invoice):
    if current_user.is_authenticated:
       total_amount = 0
       total = 0
       customer_id = current_user.id
       customer = User.query.filter_by(id=customer_id).first()
       orders = Userorder.query.filter_by(customer_id=customer_id).order_by(Userorder.id.desc()).first()
       if isinstance(orders.orders, dict):  # Check if orders.orders is a dictionary
        # Check if 'price' key exists in the dictionary
        if 'price' in orders.orders and 'quantity' in orders.orders:
            # Access the price and quantity of the product
            total_amount += (orders.orders['price'] * orders.orders['quantity'])
            total += (orders.orders['price'] * orders.orders['quantity'])
    else:
        return redirect(url_for('orders'))
       
    return render_template('root/order_details.html', invoice=invoice, customer=customer, total=total, total_amount=total_amount, orders=orders)