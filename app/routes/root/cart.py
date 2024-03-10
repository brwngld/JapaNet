from flask import render_template, redirect, url_for, flash, request, current_app, session
from app import app, db
from app.models.products import Addproduct, Brand, Category
from app.models.admin import Admin
from app.forms.admin.product import AddproductForm



@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        print("Product ID:", product_id)
        print("Quantity:", quantity)
        print("Colors:", colors)
        
        product = Addproduct.query.filter_by(id=product_id).first()
        print("Product:", product)
        
        # Print session data before adding item
        print("Session data before adding item:", session.get('Shoppingcart'))

        if product_id and quantity and colors and product:
            DicItems = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount,
                                      'color': colors, 'quantity': quantity, 'image': product.image_1}}
            print("Item to be added to cart:", DicItems)
            
            if 'Shoppingcart' in session:
                session['Shoppingcart'].update(DicItems)
            else:
                session['Shoppingcart'] = DicItems

        # Print session data after adding item
        print("Session data after adding item:", session.get('Shoppingcart'))
    
    except Exception as e:
        flash('An error occurred while adding the item to the cart', 'error')
        print("Error:", e)
        
    finally:
        return redirect(request.referrer)
