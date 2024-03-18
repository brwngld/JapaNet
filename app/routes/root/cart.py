from flask import render_template, redirect, url_for, flash, request, current_app, session
from app import app, db
from app.models.products import Addproduct, Brand, Category
from app.models.user import User, Userorder
from app.forms.admin.product import AddproductForm
from app.routes.root.user import brands, categories


def MergerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
       
        
        product = Addproduct.query.filter_by(id=product_id).first()
               
        if product_id and quantity and colors and product:
            item_details = {
                'name': product.name,
                'price': product.price,
                'discount': product.discount,
                'color': colors,
                'quantity': quantity,
                'image': product.image_1
            }
            # Calculate discounted price
            if product.discount > 0:
                discounted_price = round(float(product.price) * (1 - (float(product.discount) / 100)), 2)
                item_details['price'] = discounted_price
                
            if 'Shoppingcart' in session:
                session['Shoppingcart'] = MergerDicts(session['Shoppingcart'], {product_id: item_details})
            else:
                session['Shoppingcart'] = {product_id: item_details}

        # Print session data after adding item
        print("Session data after adding item:", session.get('Shoppingcart'))
    
    except Exception as e:
        flash('An error occurred while adding the item to the cart', 'error')
        print("Error:", e)
        
    finally:
        return redirect(request.referrer)

    
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                break  # Exit loop once item is found and removed
        return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))



@app.route('/shopcarts')
def getCart():
    if 'Shoppingcart' not in session:
        
        return redirect(request.referrer)   
    
    return render_template('root/shopcart.html', brands=brands(), categories=categories())



@app.route('/emptycarts')
def emptyCart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)


@app.route('/emptycarts')
def clearCart():
    try:
        session.pop('Shoppingcart', None)
        flash('Shopping cart cleared successfully', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        flash('An error occurred while clearing the shopping cart', 'error')
        print(e)
