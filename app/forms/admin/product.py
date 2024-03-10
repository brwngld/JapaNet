from flask_wtf import FlaskForm
from wtforms import StringField, validators, DecimalField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileAllowed, FileField

class AddproductForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()] )
    price = DecimalField('Price', [validators.DataRequired()] )
    discount = IntegerField('Discount', default= 0 )
    stock = IntegerField('Stock', [validators.DataRequired()] )
    description = TextAreaField('Description', [validators.DataRequired()] )
    colors = TextAreaField("Colors", [validators.DataRequired()] )

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please.')])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please.')])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only please.')])