from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask_migrate import Migrate
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_msearch import Search



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
db = SQLAlchemy(app) #Databse
bcrypt = Bcrypt(app) #Bcrypt for password hashing
migrate = Migrate(app, db) #Migrate database to match current database

#search tool configuration
search = Search(db=db)
search.init_app(app)

#login Manager for Users
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'user_login'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please login first"

# Define the user loader function for Flask-Login
@login_manager.user_loader
def user_loader(user_id):
    from app.models.user import User
    return User.query.get(user_id)


# Import other parts of the application
from app.routes.admin import *
from app.models.admin import *
from app.routes.root import *
from app.models.user import *
