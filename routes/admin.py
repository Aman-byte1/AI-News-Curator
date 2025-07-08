
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User
from functools import wraps # Import wraps from functools

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """
    Decorator to restrict access to admin users only.
    """
    @wraps(f) # Use @wraps to preserve the original function's name and docstring
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/manage_media')
@admin_required
def manage_media(): # Endpoint name is 'admin.manage_media'
    """
    Admin page to manage media users (approve/revoke media role).
    Displays all users who are not 'admin'.
    """
    users_to_manage = User.query.filter(User.role != 'admin').all()
    return render_template('admin/manage_media.html', title='Manage Media Access', users=users_to_manage)

@admin_bp.route('/grant_media/<int:user_id>')
@admin_required
def grant_media(user_id): # Endpoint name is 'admin.grant_media'
    """
    Grants 'media' role to a user.
    """
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot change role of an administrator.', 'danger')
    elif user.role == 'media':
        flash(f'{user.username} is already a media user.', 'info')
    else:
        user.role = 'media'
        db.session.commit()
        flash(f'Successfully granted media access to {user.username}.', 'success')
    return redirect(url_for('admin.manage_media'))

@admin_bp.route('/revoke_media/<int:user_id>')
@admin_required
def revoke_media(user_id): # Endpoint name is 'admin.revoke_media'
    """
    Revokes 'media' role from a user, setting them back to 'reader'.
    """
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot change role of an administrator.', 'danger')
    elif user.role == 'reader':
        flash(f'{user.username} is already a regular reader.', 'info')
    else:
        user.role = 'reader'
        db.session.commit()
        flash(f'Successfully revoked media access from {user.username}.', 'success')
    return redirect(url_for('admin.manage_media'))
