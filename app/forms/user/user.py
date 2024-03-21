from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed, FileField, ValidationError
from app.models.user import User

class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    number = StringField('Number', validators=[DataRequired(), Length(min=4, max=50)])
    country = StringField('Country', validators=[DataRequired(), Length(min=4, max=25)])
    state = StringField('State', validators=[DataRequired(), Length(min=4, max=25)])
    city = StringField('City', validators=[DataRequired(), Length(min=4, max=25)])
    address = StringField('Address', validators=[DataRequired(), Length(min=4, max=25)])
    
    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please.')])
    submit = SubmitField('Register')


class UserLoginForm(FlaskForm):
    email_or_username = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

