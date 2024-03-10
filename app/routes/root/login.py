from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms.user import UserRegistrationForm, UserLoginForm
from app.models.user import User
from flask_login import login_user




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
                email=email
            )
            new_user.set_password(password)

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('user_login'))

    return render_template('user/register.html', form=form, title="User Registration")


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data

        # Check if the user exists in the database
        user = User.query.filter((User.email == email)).first()

        if user and user.check_password(password):
            # Login the user
            login_user(user)

            # Redirect to the admin dashboard or any desired page
            return redirect(url_for('user_home'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('root/login.html', form=form, title="User Login")
