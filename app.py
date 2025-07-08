from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config
from models import db, User
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
from datetime import datetime # Import datetime

def create_app():
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Redirect to login page if not authenticated
    login_manager.login_message_category = 'info' # Category for login required message

    @login_manager.user_loader
    def load_user(user_id):
        """
        Loads a user from the database given their ID.
        Required by Flask-Login.
        """
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

        # Optional: Create a default admin user if none exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', email='admin@example.com', role='admin')
            admin_user.set_password('adminpassword') # Set a strong password in production!
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created: username='admin', password='adminpassword'")

    # Context processor to make current_year available in all templates
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Custom error handler for 404 Not Found errors.
        """
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """
        Custom error handler for 500 Internal Server Errors.
        """
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) # Run in debug mode for development