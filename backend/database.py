"""
Database initialization module for the Todo application.
Sets up SQLAlchemy database connection with SQLite.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask application.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database initialized successfully!")

# Made with Bob