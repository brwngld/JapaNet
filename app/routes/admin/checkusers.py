from app import app, db
from app.models.admin import Admin
from app.models.user import User
from flask import render_template, redirect, url_for, flash


@app.route('/users/list')
def users():
    users = User.query.all()
    admins = Admin.query.all()
    return render_template('admin/checkusers.html', users=users, admins=admins)


@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('users'))


@app.route('/admin/delete/<int:admin_id>', methods=['POST'])
def delete_admin(admin_id):
    admin = Admin.query.get_or_404(admin_id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin user deleted successfully', 'success')
    return redirect(url_for('users'))