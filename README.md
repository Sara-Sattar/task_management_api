# Task Management API

This is a simple **Task Management API** built with **Django REST Framework**, allowing users to manage their own tasks securely using **JWT authentication**.

## Features
- User registration and authentication (JWT)
- CRUD operations for tasks (Create, Read, Update, Delete)
- Mark tasks as completed with timestamps
- Filtering by status, priority, and due date
- Secure access — users only see their own tasks


**Create and activate virtual environment**
   python -m venv .venv
   source .venv/bin/activate  

**Apply migrations**
    python manage.py migrate

**Run development server**
    python manage.py runserver

API available at: http://127.0.0.1:8000/

### Authentification
POST  `/api/token/` 

### Utilisateurs
GET : `/api/users/` -> List all users
POST : `/api/users/` -> Create a new user
GET : `/api/users/{id}/` -> Retrieve user details
PUT/PATCH : `/api/users/{id}/` -> Update user information
DELETE : `/api/users/{id}/` -> Delete a user

### Tasks
GET:`/api/tasks/` -> List all tasks
POST : `/api/tasks/` -> Create a new task
GET : `/api/tasks/{id}/` -> Retrieve task details
PUT/PATCH : `/api/tasks/{id}/` -> Update a task
DELETE : `/api/tasks/{id}/` -> Delete a task
PATCH : `/api/tasks/{id}/complete/` -> Mark or unmark a task as completed

### Query Parameters (Tasks)
status: Filter by task status (Pending, Completed)
priority: Filter by task priority (Low, Medium, High)
due_date: Filter by due date (YYYY-MM-DD or ISO datetime)

## Security Notes
- All endpoints require JWT authentication
-Users can only access their own tasks
-Completed tasks cannot be edited unless reverted to “Pending”
-Access tokens expire after 60 minutes (configurable)
-Refresh tokens expire after 7 days


