from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), unique = False, nullable = False)
    last_name = db.Column(db.String(30), unique = False, nullable = False)
    company_name = db.Column(db.String(180), unique = True, nullable = False)
    nature_of_business = db.Column(db.String(120), unique = True, nullable = False)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(180), unique = False, nullable = False)
   

    def __repr__(self):
        return f'<Admin {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    