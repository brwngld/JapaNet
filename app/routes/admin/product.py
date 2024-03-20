from app import app, db, photos
from flask import redirect, render_template, url_for, flash, request,current_app, session
from app.models.products import Brand, Category, Addproduct
from app.forms.admin import AddproductForm
from werkzeug.utils import secure_filename
import secrets
import os



#Brand Routes
@app.route('/admin/addbrand', methods=['GET', 'POST'])
def add_brand():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        getbrand = request.form.get('name')
        # Check if the brand already exists in the database
        existing_brand = Brand.query.filter_by(name=getbrand).first()
        if existing_brand:
            flash(f'The Brand {getbrand} already exists in the database', 'warning')
        else:
            brand = Brand(name=getbrand)
            db.session.add(brand)
            flash(f'The Brand {getbrand} was added to your database', 'success')
            db.session.commit()
       
        return redirect (url_for('add_brand'))
    
    return render_template('admin/addbrand.html')



#Displays list of all brands
@app.route('/admin/brands', methods=['GET', 'POST'])
def brands():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    brands = Brand.query.order_by(Brand.id.desc()).all()
    
    return render_template('admin/brand.html', title="Brands Page", brands=brands)

#Updates the brand names existing in the database
@app.route('/admin/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    updatebrand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        brand = request.form.get('name')
        updatebrand.name = brand
        flash('Your brand was updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('admin/updatebrand.html', title='Update Brand page', updatebrand=updatebrand)


#Deletes the brands from the datatase
@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('brands'))
    flash(f"The brand {brand.name} can't be deleted", 'warning')
    return redirect(url_for('brands'))






#Category Routes
@app.route('/admin/addcategory', methods=['GET', 'POST'])
def add_category():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        getcategory = request.form.get('name')
        # Check if the category already exists in the database
        existing_category = Category.query.filter_by(name=getcategory).first()
        if existing_category:
            flash(f'The Category {getcategory} already exists in the database', 'warning')
        else:
            category = Category(name=getcategory)
            db.session.add(category)
            flash(f'The Category {getcategory} was added to your database', 'success')
            db.session.commit()
        
        return redirect (url_for('add_category'))
    
    return render_template('admin/addcategory.html')


#Displays list of all categories in the database
@app.route('/admin/categories', methods=['GET', 'POST'])
def categories():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    categories = Category.query.order_by(Category.id.desc()).all()
    
    
    return render_template('admin/category.html', title="Categories Page", categories=categories)


#Updates the category names existing in the database
@app.route('/admin/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        category = request.form.get('name')  # Corrected attribute name to 'name'
        updatecat.name = category
        flash(f'Your category was updateded succesfully', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('admin/updatecategory.html', title='Update Category page', updatecat=updatecat)


#Deletes the cateogory name exiting in the database
@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('categories'))
    flash(f"The brand {category.name} can't be deleted", 'warning')
    return redirect(url_for('categories'))




#Proucts Routes
@app.route('/admin/addproduct', methods=['GET', 'POST'])
def add_product():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddproductForm(request.form)
    
    if request.method == 'POST':
        # Retrieve user email from session
        admin_email = session['email']
        
        # Retrieve form data
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        colors = form.colors.data
        brand = request.form.get('brand')
        category  = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        
        # Create Addproduct object and associate with user
        addpro = Addproduct(
            name=name, price=price, discount=discount, stock=stock, description=description, 
            colors=colors, brand_id=brand, category_id=category, 
            image_1=image_1, image_2=image_2, image_3=image_3,
            admin_email=admin_email  # Associate product with user
        )
        
        db.session.add(addpro)
        db.session.commit()
        
        flash(f'The product {name} has been added successfully', 'success')
        
    return render_template('admin/addproduct.html', form=form, title='Add product', brands=brands, categories=categories)

#----------------------------------------------------------------------------------------------------------------


@app.route('/admin/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)

    if product.admin_email != session['email']:
        flash('You are not authorized to update this product.', 'danger')
        return redirect(url_for('admin_home'))
    

    brand = request.form.get('brand')
    category = request.form.get('category')
    
    form = AddproductForm(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.description = form.description.data
        
        
        # Check if new images are uploaded
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                flash('Error occurred while uploading Image 1.', 'error')

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                flash('Error occurred while uploading Image 2.', 'error')

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                flash('Error occurred while uploading Image 3.', 'error')

        db.session.commit()
        flash('Your product has been updated successfully.', 'success')
        return redirect(url_for('admin_home'))
   
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description
    return render_template('admin/updateproduct.html', form=form, brands=brands, categories=categories, product=product)


#----------------------------------------------------------------------------------------------------------------

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('admin_login'))
    
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted from your database', 'success')
        return redirect(url_for('admin_home'))
    flash(f"The product {product.name} can't be deleted", 'warning')
    return redirect(url_for('admin_home'))


#----------------------------------------------------------------------------------------------------------------