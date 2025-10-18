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

### users
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
due_date: Filter by due date 

## Security Notes
- All endpoints require JWT authentication
-Users can only access their own tasks
-Completed tasks cannot be edited unless reverted to “Pending”
-Access tokens expire after 60 minutes (configurable)
-Refresh tokens expire after 7 days


###user endpoint
1. *Create a user* :

*POST* /api/users/
*Request Body*
JSON:
{
    "username": "alice",
    "email": "alice@example.com",
    "password": "StrongPass123!"
}
2. *view profile*
*GET* /api/users/

3. *Update email*
*PATCH* /api/users/<id>/ 


###Get JWT tokens 
*POST* /api/token/
*Request Body*
JSON:
{
    "username": "alice",
    "password": "StrongPass123!"
}
###Tasks Endpoints

1.*list tasks*
*GET* /api/tasks/  

2.*create Task*
*POST* /api/tasks/create/
*Request Body*
JSON:
{
    "title": "Buy groceries",
    "description": "Get vegetables and fruits",
    "priority": "Medium",
    "due_date": "2025-10-18"
}

3.*Update*
*PATCH* /api/tasks/<id>/
*Request Body*
JSON:
{
    "description": "Get vegetables, fruits, and bread"
}

4.*mark it as completed*
*PATCH* /api/tasks/<id>/complete/
*Request Body*
JSON:
{ "completed": true }

5.*Editing a completed task*
*PATCH* /api/tasks/<id>/ 
5.1: *Result* 400 Bad Request

6. *FILTERING*
6.1: *By status*
*GET* /api/tasks/?status=Pending
6.2: *By priority*
*GET* /api/tasks/?priority=High
6.3: *By due_date*
*GET* /api/tasks/?due_date=2025-10-20

7. *DELETION*
7.1: *delete task*
*DELETE* /api/tasks/<id>/
*Result* : 204 No Content

7.2: *Check deletion* :
*GET* /api/tasks/<id>/ 
*Result* :404 Not Found