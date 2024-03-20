from flask import render_template, redirect, url_for, flash, request
from app import app, db, search
from app.models.products import Addproduct, Brand, Category


#A function to retrieve all brands from the database
def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

#A function to retrieve all categories from the database
def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories



#Display a list of products associated with a specific brand to the user
@app.route('/brand/<int:id>')
def get_brand(id):
    #Retrieve the current page number from the URL query parameters
    page = request.args.get('page', 1, type=int)
    
    #Fetch the brand with the specified ID from the database, or return a 404 error if not found
    get_bran = Brand.query.filter_by(id=id).first_or_404()
    
    #Query the 'Addproduct' table in the database to retrieve products associated with the specified brand
    brand = Addproduct.query.filter_by(brand_id=get_bran.id).paginate(page=page, per_page=6)
   
    return render_template('root/brands.html', brand=brand, brands=brands(), categories=categories(), get_bran=get_bran)


#Display a list of products associated with a specific category to the user
@app.route('/category/<int:id>')
def get_cat(id):
    #Retrieve the current page number from the URL query parameters
    page = request.args.get('page', 1, type=int)
    
    #Fetch the category with the specified ID from the database, or return a 404 error if not found
    get_categ = Category.query.filter_by(id=id).first_or_404()
   
    #Query the 'Addproduct' table in the database to retrieve products associated with the specified category
    category = Addproduct.query.filter_by(category_id=get_categ.id).order_by(
        Addproduct.id.desc()).paginate(page=page, per_page=6)
    
    return render_template('root/categories.html', category=category, categories=categories(), brands=brands(), get_categ=get_categ)




#Customer's Homepage routes
@app.route('/')
@app.route('/home')
def home():
    #Retrieve the current page number from the URL query parameters
    page = request.args.get('page', 1, type=int)
   
    #Query the database for products with positive stock levels and order them by ID in descending order
    products = Addproduct.query.filter(Addproduct.stock >= 0).order_by(
        Addproduct.id.desc()).paginate(page=page, per_page=6)        
    return render_template('root/index.html', products=products, brands=brands(), categories=categories())





@app.route('/details/<int:id>')
def detail_page(id):
    #Displays details of single products
    product = Addproduct.query.get_or_404(id)
        
    #Determine whether to display "Out of Stock" or "Add to Cart" button
    if product.stock > 0:
        button_text = "Out of Stock"
    else:
        button_text = "Add to Cart"
        
    return render_template('root/details.html', product=product, button_text=button_text, brands=brands(), categories=categories() )


#---------------------------------------------------------------------

"""SEARCH ALGORITHM"""
@app.route('/result')
def result():
    #Retrieve the search query from the URL query parameters"""
    searchword = request.args.get('query')
    
    #Retrieve the current page number from the URL query parameters, with a default value of 1
    page = request.args.get('page', 1, type=int)
    
    #Set the number of items per page
    per_page = 6
    
    #Query the database for products matching the search query
    if searchword:
        pagination = Addproduct.query.filter(
            (Addproduct.name.ilike(f'%{searchword}%')) |
            (Addproduct.description.ilike(f'%{searchword}%')) |
            (Addproduct.price == searchword) |
            (Addproduct.brand.has(name=searchword)) |
            (Addproduct.category.has(name=searchword))
        ).paginate(page=page, per_page=per_page)
    else:
        #If no search query provided, return all products
        pagination = Addproduct.query.paginate(page=page, per_page=per_page)
    
    #Check if products is empty
    if not pagination.items:
        #Redirect to a "not found" page if no products are found matching the search query
        return redirect(url_for('not_found'))

    return render_template('root/result.html', pagination=pagination, brands=brands(), categories=categories())

#Displays the 'Not Found' template when the search query does not match any product in the database.
@app.route('/not_found')
def not_found():
    return render_template('root/404.html', title='Not Found')