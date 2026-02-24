"""
Database models for the Todo application.
Defines the Todo model with SQLAlchemy ORM.
"""

from datetime import datetime
from database import db


class Todo(db.Model):
    """
    Todo model representing a single todo item.
    
    Attributes:
        id: Unique identifier (primary key)
        title: Todo title (required)
        description: Detailed description (optional)
        completed: Completion status (default: False)
        created_at: Timestamp when todo was created
        updated_at: Timestamp when todo was last updated
    """
    
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """
        Convert Todo object to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the Todo object
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of Todo object."""
        return f'<Todo {self.id}: {self.title}>'

# Made with Bob