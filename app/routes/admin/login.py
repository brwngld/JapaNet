from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.forms.admin import RegistrationForm, LoginForm
from app.models.products import Brand, Category, Addproduct
from app.models import Admin




@app.route('/admin/home', methods=['GET', 'POST'])
def admin_home():
      
    if 'email' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin_email = session['email']  # Get the logged-in user's email from the session

    products = Addproduct.query.filter_by(admin_email=admin_email).all()

    # Get the logout URL
    logout_url = url_for('admin_logout')

    # If it's a GET request, render the admin dashboard template
    return render_template('admin/index.html', title="Admin Dashboard", products=products, logout_url=logout_url)



@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    form = RegistrationForm()
    if request.method == 'POST':
        # Extract data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        company_name = form.company_name.data
        nature_of_business = form.nature_of_business.data
        email = form.email.data
        password = form.password.data

        # Check if the email or username already exists
        existing_admin_email = Admin.query.filter_by(email=email).first()
        

        if existing_admin_email:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('admin_register'))
        elif Admin.query.filter_by(company_name=company_name).first():
            flash('Company name already exists. Please choose a different company name.', 'danger')
            return redirect(url_for('admin_register'))
        else:
            # Create a new Admin object
            new_admin = Admin(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                nature_of_business=nature_of_business,
                email=email
            )
            new_admin.set_password(password)

            # Add the new admin to the database
            db.session.add(new_admin)
            db.session.commit()

            # Redirect to a success page or login page
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('admin_home'))

    return render_template('admin/register.html', form=form, title="Admin Registration")


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data

        # Check if the user exists in the database
        admin = Admin.query.filter((Admin.email == email)).first()

        if admin and admin.check_password(password):
            session['email'] = email  # Add the email to the session
            flash(f'Welcome {form.email.data}. You are logged in now', 'success')
            
            return redirect(url_for('admin_home'))  # Redirect to admin_home on successful login         
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('admin/login.html', form=form, title="Admin Login")




@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    if request.method == 'POST':
        if 'email' in session:
            # Clear the session
            session.clear()
            # Flash a message to notify the user
            flash('You have been logged out successfully.', 'success')
            # Redirect to the admin login page regardless of whether the user was logged in or not
            
    return redirect(url_for('admin_login'))