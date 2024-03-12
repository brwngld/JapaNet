from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models.user import User
from app.models.products import Addproduct, Brand, Category
from flask_login import login_required

from flask_login import login_user


def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()  # Retrieve all brands from the database
    return brands


def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_bran = Brand.query.filter_by(id=id).first_or_404()
    # Query database for products with the specified brand_id
    brand = Addproduct.query.filter_by(brand_id=get_bran.id).paginate(page=page, per_page=6)
   
    return render_template('root/brands.html', brand=brand, brands=brands(), categories=categories(), get_bran=get_bran)



@app.route('/category/<int:id>')
def get_cat(id):
    page = request.args.get('page', 1, type=int)
    get_categ = Category.query.filter_by(id=id).first_or_404()
    # Query database for products with the specified category_id
    category = Addproduct.query.filter_by(category_id=get_categ.id).order_by(
        Addproduct.id.desc()).paginate(page=page, per_page=6)
    
    return render_template('root/categories.html', category=category, categories=categories(), brands=brands(), get_categ=get_categ)




#homepage routes
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock >= 0).order_by(
        Addproduct.id.desc()).paginate(page=page, per_page=6)        
    return render_template('root/index.html', products=products, brands=brands(), categories=categories())






@app.route('/details/<int:id>')
def detail_page(id):
    product = Addproduct.query.get_or_404(id)
        
    # Determine whether to display "Out of Stock" or "Add to Cart" button
    if product.stock >= 0:
        button_text = "Out of Stock"
    else:
        button_text = "Add to Cart"
        
    return render_template('root/details.html', product=product, button_text=button_text, brands=brands(), categories=categories() )
