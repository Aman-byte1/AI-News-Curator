import os

class Config:
    """
    Configuration settings for the Flask application.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_you_should_change'
    # Database configuration: Using SQLite for simplicity.
    # 'sqlite:///site.db' creates a file named site.db in the project root.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable tracking modifications for performance