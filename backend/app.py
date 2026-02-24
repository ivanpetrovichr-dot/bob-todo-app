"""
Main Flask application for the Todo API.
Provides RESTful endpoints for managing todos with CORS enabled.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, init_db
from models import Todo


# Initialize Flask application
app = Flask(__name__)

# Get absolute path for database
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

# Configuration - use absolute path for SQLite
db_path = os.path.join(instance_path, 'todos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for all routes
CORS(app)

# Initialize database
init_db(app)


# ============================================================================
# API Routes
# ============================================================================

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """
    Get all todos.
    
    Returns:
        JSON response with list of all todos
    """
    try:
        todos = Todo.query.order_by(Todo.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [todo.to_dict() for todo in todos]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """
    Get a specific todo by ID.
    
    Args:
        todo_id: ID of the todo to retrieve
        
    Returns:
        JSON response with the todo data
    """
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': todo.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """
    Create a new todo.
    
    Expected JSON body:
        {
            "title": "Todo title (required)",
            "description": "Todo description (optional)"
        }
        
    Returns:
        JSON response with the created todo
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'title' not in data or not data['title'].strip():
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        # Create new todo
        new_todo = Todo(
            title=data['title'].strip(),
            description=data.get('description', '').strip() or None
        )
        
        db.session.add(new_todo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_todo.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """
    Update an existing todo.
    
    Args:
        todo_id: ID of the todo to update
        
    Expected JSON body (all fields optional):
        {
            "title": "Updated title",
            "description": "Updated description",
            "completed": true/false
        }
        
    Returns:
        JSON response with the updated todo
    """
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Update fields if provided
        if 'title' in data:
            if not data['title'].strip():
                return jsonify({
                    'success': False,
                    'error': 'Title cannot be empty'
                }), 400
            todo.title = data['title'].strip()
        
        if 'description' in data:
            todo.description = data['description'].strip() or None
        
        if 'completed' in data:
            todo.completed = bool(data['completed'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': todo.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    Delete a todo.
    
    Args:
        todo_id: ID of the todo to delete
        
    Returns:
        JSON response confirming deletion
    """
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        db.session.delete(todo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Todo deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/todos/<int:todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id):
    """
    Toggle the completion status of a todo.
    
    Args:
        todo_id: ID of the todo to toggle
        
    Returns:
        JSON response with the updated todo
    """
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({
                'success': False,
                'error': 'Todo not found'
            }), 404
        
        # Toggle completed status
        todo.completed = not todo.completed
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': todo.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# Health Check & Root Route
# ============================================================================

@app.route('/')
def index():
    """Root endpoint - API information."""
    return jsonify({
        'message': 'Todo API is running',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/todos': 'Get all todos',
            'GET /api/todos/<id>': 'Get specific todo',
            'POST /api/todos': 'Create new todo',
            'PUT /api/todos/<id>': 'Update todo',
            'DELETE /api/todos/<id>': 'Delete todo',
            'PATCH /api/todos/<id>/toggle': 'Toggle todo completion'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


# ============================================================================
# Run Application
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Todo API Server Starting...")
    print("=" * 60)
    print("Server running at: http://localhost:5005")
    print("API endpoints available at: http://localhost:5005/api/todos")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5005)

# Made with Bob