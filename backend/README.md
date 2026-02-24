# Todo App - Flask Backend

A simple RESTful API backend for a todo application built with Flask and SQLAlchemy.

## Features

- ✅ RESTful API with CRUD operations
- ✅ SQLite database (no installation required)
- ✅ CORS enabled for frontend communication
- ✅ Simple and clean code structure
- ✅ JSON responses with proper error handling

## Project Structure

```
backend/
├── app.py              # Main Flask application with API routes
├── models.py           # SQLAlchemy Todo model
├── database.py         # Database initialization
├── requirements.txt    # Python dependencies
└── instance/
    └── todos.db       # SQLite database (auto-generated)
```

## Prerequisites

- Python 3.12 or 3.13
- pip (Python package manager)

## Installation & Setup

### 1. Navigate to backend directory

```bash
cd todo-app/backend
```

### 2. Create virtual environment

```bash
python3 -m venv venv
```

### 3. Activate virtual environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The server will start at: **http://localhost:5005**

You should see:
```
============================================================
Todo API Server Starting...
============================================================
Server running at: http://localhost:5005
API endpoints available at: http://localhost:5005/api/todos
Press CTRL+C to stop the server
============================================================
```

## API Endpoints

### Base URL: `http://localhost:5005/api`

| Method | Endpoint                    | Description              |
|--------|----------------------------|--------------------------|  
| GET    | `/todos`                   | Get all todos            |
| GET    | `/todos/<id>`              | Get specific todo        |
| POST   | `/todos`                   | Create new todo          |
| PUT    | `/todos/<id>`              | Update todo              |
| DELETE | `/todos/<id>`              | Delete todo              |
| PATCH  | `/todos/<id>/toggle`       | Toggle completion status |

### Example Requests

#### 1. Get all todos
```bash
curl http://localhost:5005/api/todos
```

#### 2. Create a new todo
```bash
curl -X POST http://localhost:5005/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

#### 3. Update a todo
```bash
curl -X PUT http://localhost:5005/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "completed": true}'
```

#### 4. Toggle completion
```bash
curl -X PATCH http://localhost:5005/api/todos/1/toggle
```

#### 5. Delete a todo
```bash
curl -X DELETE http://localhost:5005/api/todos/1
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-24T09:00:00",
    "updated_at": "2026-02-24T09:00:00"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Todo not found"
}
```

## Database Schema

### Todo Table

| Column      | Type         | Constraints                    |
|-------------|--------------|--------------------------------|
| id          | INTEGER      | PRIMARY KEY, AUTOINCREMENT     |
| title       | VARCHAR(200) | NOT NULL                       |
| description | TEXT         | NULLABLE                       |
| completed   | BOOLEAN      | DEFAULT FALSE                  |
| created_at  | DATETIME     | DEFAULT CURRENT_TIMESTAMP      |
| updated_at  | DATETIME     | DEFAULT CURRENT_TIMESTAMP      |

## Testing the API

You can test the API using:

1. **cURL** (command line)
2. **Postman** (GUI application)
3. **Thunder Client** (VS Code extension)
4. **Browser** (for GET requests)

### Quick Test

Visit http://localhost:5005 in your browser to see API information.

## Troubleshooting

### Port already in use
If port 5005 is already in use, modify the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5006)  # Change to 5006
```

### Database issues
Delete the database file and restart:
```bash
rm instance/todos.db
python app.py
```

### Import errors
Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # Activate venv
pip install -r requirements.txt
```

## Development

### Debug Mode
Debug mode is enabled by default. To disable:
```python
app.run(debug=False, host='0.0.0.0', port=5005)
```

### Database Location
The SQLite database is stored in `instance/todos.db` and is automatically created on first run.

## Next Steps

1. ✅ Backend is complete
2. Create frontend (HTML/CSS/JavaScript)
3. Connect frontend to backend API
4. Test the complete application

## License

MIT License - Feel free to use this code for learning and projects.