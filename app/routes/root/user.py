from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models.user import User
from app.models.products import Addproduct, Brand, Category

from flask_login import login_user


@app.route('/brand/<int:id>')
def get_brand(id):
    # Query database for products with the specified brand_id
    brand = Addproduct.query.filter_by(brand_id=id).all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()  # Retrieve all brands from the database
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('root/brands.html', brand=brand, brands=brands, categories=categories)

@app.route('/category/<int:id>')
def get_cat(id):
    # Query database for products with the specified brand_id
    category = Addproduct.query.filter_by(category_id=id).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()  # Retrieve all brands from the database

    return render_template('root/categories.html', category=category, categories=categories, brands=brands)



#homepage routes
@app.route('/')
@app.route('/home')
def home():
    products = Addproduct.query.filter(Addproduct.stock >= 0)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
        
    return render_template('root/index.html', products=products, brands=brands, categories=categories)


from flask_login import login_required




@app.route('/account')
@login_required
def account():
    # Logic to retrieve and display account information for the current user
    return render_template('account.html')

