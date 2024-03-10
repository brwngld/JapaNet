from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads
from decimal import Decimal  # Importing Decimal from the decimal module


# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)


# Obtain the base directory path of the application
basedir = os.path.abspath(os.path.dirname(__file__))


photos = UploadSet('photos', IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir, 'static/img')
configure_uploads(app, photos)


# Set up the secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Set up the database URI from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Initialize Flask extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'admin_login'  # Set the login view for Flask-Login
migrate = Migrate(app, db)


# Define the user loader function for Flask-Login
@login.user_loader
def load_user(user_id):
    from app.models.admin import Admin
    from app.models.user import User

    # Check if the user ID corresponds to an admin or a regular user
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    else:
        return User.query.get(int(user_id))

# Import other parts of the application
from app.routes.admin import *
from app.models.admin import *
from app.routes.root import *


# Example of using session
@app.route('/set-session')
def set_session():
    session['key'] = 'value'
    return 'Session set'

@app.route('/get-session')
def get_session():
    return session.get('key', 'Session key not found')