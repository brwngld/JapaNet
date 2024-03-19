from app import app, db
from flask import redirect, render_template, url_for, flash, request, session
from app.models.user import Userorder, User




@app.route('/admin/orders')
def admin_orders():
    # Check if the user is logged in as an administrator
    if 'email' not in session:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('admin_login'))  # Redirect to login page or another page

    # Query the database to get all orders
    orders = Userorder.query.all()

    return render_template('admin/orders.html', orders=orders)




@app.route('/admin/orders/<int:order_id>')
def admin_order_details(order_id):
    # Check if the user is logged in as an administrator
    if 'email' not in session:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('admin_login'))  # Redirect to the login page or another page

    # Retrieve the order from the database
    order = Userorder.query.get_or_404(order_id)

    # Retrieve customer information based on customer_id associated with the order
    customer = User.query.get(order.customer_id)

    # Calculate subtotal and grand total
    subtotal = sum(float(item['price']) * int(item['quantity']) for item in order.orders.values())
    grandtotal = round(subtotal, 2)

    return render_template('admin/order_details.html', order=order, subtotal=subtotal, grandtotal=grandtotal, customer=customer)



@app.route('/admin/orders/<int:order_id>/change_status', methods=['POST'])
def change_order_status(order_id):
    # Check if the user is logged in as an administrator
    if 'email' not in session:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('admin_login'))  # Redirect to login page or another page

    # Retrieve the order from the database
    order = Userorder.query.get_or_404(order_id)

    # Get the new status from the form data
    new_status = request.form.get('status')

    # Update the order status
    order.status = new_status
    db.session.commit()

    flash('Order status updated successfully.', 'success')
    return redirect(url_for('admin_orders'))

