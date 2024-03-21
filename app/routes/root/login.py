from flask import render_template, redirect, url_for, flash, request, session, make_response
from app import app, db, login_manager
from app.forms.user import UserRegistrationForm, UserLoginForm
from app.models.user import User, Userorder
from app.models.products import Addproduct
from flask_login import login_required, current_user, logout_user, login_user
import secrets
from app.routes.root.user import brands, categories
import pdfkit
from pdfkit.configuration import Configuration


#Route to handle customer registration
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        """Extract data from the form"""
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        number = form.number.data
        country = form.country.data
        state = form.state.data
        city = form.city.data
        address = form.address.data
    
        #Check if the email or username already exists in the database
        existing_user_email = User.query.filter_by(email=email).first()
        existing_user_username = User.query.filter_by(username=username).first()

        if existing_user_email:
            flash('Email already exists. Please use a different email.', 'error')
        elif existing_user_username:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            #Create a new User object
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                number=number,
                country=country,
                state=state,
                city=city,
                address=address
            )
            new_user.set_password(password)

            #Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            
            #Provide feedback to the user and redirect to the login page
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('user_login'))
        
    #Render the registration form template
    return render_template('root/register.html', form=form, title="User Registration")

#----------------------------------------------------------------------------------------------------------------------------

#Route to handle customer login
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    if form.validate_on_submit():
        #Extract email/username and password from the login form"""
        email_or_username = form.email_or_username.data
        password = form.password.data

        #Check if the provided email/username exists in the database
        user = User.query.filter_by(email=email_or_username).first() or User.query.filter_by(username=email_or_username).first()
        
        
        if user and user.check_password(password):
            #If user exists and password matches, log the user in
            
            login_user(user)
            flash(f'Welcome {email_or_username}. You are logged in now', 'success')
            return redirect(url_for('home'))
        else:
            #If email/username or password is incorrect, provide feedback to the user
            
            flash('Invalid email/username or password combination.', 'danger')
            return redirect(url_for('user_login'))

    return render_template('root/login.html', form=form, title="User Login")

#-------------------------------------------------------------------------------------------------------------------------------------

#Route to handle customer logout
@app.route('/user/logout', methods=['POST'])
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))


#-------------------------------------------------------------------------------------------------------------------------------------

#Route to handle customers order
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        
        try:
            #Create Userorder instance with updated orders
            order_items = session.get('Shoppingcart', {})
            for product_id, item_details in order_items.items():
                quantity_ordered = int(item_details.get('quantity', 0))
                
                #Update product stock in the database
                product = Addproduct.query.get(product_id)
                
                if product:
                    #Check if the requested quantity exceeds the available stock
                    if quantity_ordered > product.stock:
                        flash(f"Insufficient stock for {product.name}. Available stock: {product.stock}", "danger")
                        return redirect(url_for('getCart'))
            
                    #Update product stock in the database
                    product.stock -= quantity_ordered
                    db.session.add(product)
            
            #Create the order after updating stock
            order = Userorder(invoice=invoice, customer_id=customer_id, orders=order_items)
            db.session.add(order)
            db.session.commit()
            
            session.pop('Shoppingcart', None)
            flash("Your order has been sent", "success")
            return redirect(url_for('orders', invoice=invoice))
        
        except Exception as e:
            print(e)
            #Rollback changes if an error occurs
            db.session.rollback()
            flash('Something went wrong while submitting order', 'danger')
            return redirect(url_for('getCart'))
        


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    #Retrieve the current user object
    customer = current_user

    #Query the database to find orders associated with the provided
    #invoice number and the current customer's ID
    orders = Userorder.query.filter_by(invoice=invoice, customer_id=current_user.id).first()
    
    #If orders are found
    if orders:
        #Calculate the subtotal by summing up the prices of 
        #individual items multiplied by their quantities
        subtotal = sum(float(item['price']) * int(item['quantity']) for item in orders.orders.values())
        #Round the subtotal to two decimal places to get the grand total
        grandtotal = round(subtotal, 2)
        return render_template('root/ordertrack.html', invoice=invoice, customer=customer, orders=orders, subtotal=subtotal, grandtotal=grandtotal, brands=brands(), categories=categories())
    else:
        #If no orders are found for the provided invoice number,
        #flash a message and redirect to the home page
        flash('No order found with the provided invoice number.', 'info')
        return redirect(url_for('home'))



@app.route('/order-history/')
@login_required
def order_history():
    #Query the database to get all orders for the current user,
    #ordered by ID in descending order
    orders = Userorder.query.filter_by(customer_id=current_user.id).order_by(Userorder.id.desc()).all()
    return render_template('root/order_history.html', orders=orders, brands=brands(), categories=categories())



@app.route('/pdf_gen/<invoice>', methods=['POST'])
@login_required
def pdf_gen(invoice):
    if request.method == "POST":
        # Retrieve the current user object
        customer = current_user
        
        # Query the database to find orders associated with the provided invoice number and the current customer's ID
        orders = Userorder.query.filter_by(invoice=invoice, customer_id=current_user.id).first()
        
        # If orders are found
        if orders:
            # Calculate the subtotal by summing up the prices of individual items multiplied by their quantities
            subtotal = sum(float(item['price']) * int(item['quantity']) for item in orders.orders.values())
            # Round the subtotal to two decimal places to get the grand total
            grandtotal = round(subtotal, 2)
            
        # Render the PDF template, passing relevant data
        rendered = render_template('root/pdf.html', invoice=invoice, customer=customer, orders=orders, subtotal=subtotal, grandtotal=grandtotal, brands=brands(), categories=categories())
        
        config = Configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

        # Generate PDF from the rendered template
        pdf = pdfkit.from_string(rendered, False, configuration=config) 
        
        # Create a response with the PDF content
        response = make_response(pdf)
        # Set the response headers for PDF content type and filename
        response.headers['content-Type'] = 'application/pdf'
        response.headers['content-Disposition'] = 'inline: filename=' + invoice + '.pdf'
        
        return response
    
    return redirect(url_for('orders'))