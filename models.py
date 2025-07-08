from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Represents a user in the system.
    Users can be 'reader', 'media', or 'admin'.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # Roles: 'reader', 'media', 'admin'
    role = db.Column(db.String(20), default='reader', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to NewsArticle: A user (media) can post many articles
    news_articles = db.relationship('NewsArticle', backref='author', lazy='dynamic')

    # Relationship to UserInteraction: A user can have many interactions
    interactions = db.relationship('UserInteraction', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

class NewsArticle(db.Model):
    """
    Represents a news article posted by a media user.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True) # e.g., 'Politics', 'Tech', 'Sports'
    source_name = db.Column(db.String(100), nullable=True) # Name of the media source
    source_url = db.Column(db.String(500), nullable=True) # URL of the original source
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign key to the User who posted the article (media user)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to UserInteraction: An article can have many interactions
    interactions = db.relationship('UserInteraction', backref='article', lazy='dynamic')

    def __repr__(self):
        return f"<NewsArticle {self.title}>"

class UserInteraction(db.Model):
    """
    Records user interactions with news articles for personalization.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('news_article.id'), nullable=False)
    # Type of interaction: 'read', 'skipped', 'liked', 'disliked', 'shared'
    interaction_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Optional: Time spent reading (in seconds)
    time_spent_seconds = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<UserInteraction User:{self.user_id} Article:{self.article_id} Type:{self.interaction_type}>"