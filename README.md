# Employee Leave Management System (Backend)

## Project Overview

The Employee Leave Management System is a REST API built using **Python, Django, and Django REST Framework**.

The system provides role-based leave management functionality for employees and managers. It also manages employee departments, allowing employees to be associated with a department during account creation.

---

## Employee Features

Employees can:

- Register and authenticate using JWT authentication.
- Apply for leave requests.
- View their own leave requests.
- Update pending leave requests.
- Delete pending leave requests.
- Filter leave requests by status and leave type.

---

## Manager Features

Managers can:

- View all employee leave requests.
- Search leave requests by employee name.
- Filter leave requests by leave type and status.
- Approve leave requests.
- Reject leave requests.

---

## Technologies Used

- Python
- Django
- Django REST Framework
- Simple JWT Authentication
- Django Filters
- drf-spectacular (Swagger/OpenAPI Documentation)
- PostgreSQL
- Docker & Docker Compose

---

# Local Development Setup

## 1. Clone the Repository

```bash
  git clone https://github.com/manishbhattrai/Employee-Leave-Management-System-Backend-.git
  
  cd Employee-Leave-Management-System-Backend-
```

---

## 2. Create Virtual Environment

```bash
  python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
  .venv\Scripts\activate
```

### Linux/Mac

```bash
  source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
  pip install -r requirements.txt
```

---

## 4. Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
SECRET_KEY=your-secret-key

DATABASE_NAME=database_name
DATABASE_USER=database_user
DATABASE_PASSWORD=database_password
DATABASE_PORT=5432

POSTGRES_DB=database_name
POSTGRES_USER=database_user
POSTGRES_PASSWORD=database_password
```

Database host depends on how the application is running:

Local development:

```env
DATABASE_HOST=localhost
```

Docker Compose:

```env
DATABASE_HOST=db
```

---

## 5. Database Migration

Run migrations:

```bash
  python manage.py migrate
```

Create a superuser:

```bash
  python manage.py createsuperuser
```

---

## 6. Run the Application

Start the development server:

```bash
  python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

---

# Docker Setup

The application supports Docker-based development using Docker Compose with PostgreSQL.

The Docker setup includes:

- Django REST Framework application container.
- PostgreSQL database container.
- Persistent PostgreSQL storage using Docker volumes.

---

## Prerequisites

Install:

- Docker
- Docker Compose

---

## Build Docker Containers

```bash
  docker compose build
```

---

## Start Application

```bash
  docker compose up
```

The API will be available at:

```
http://localhost:8000/
```

---

## Run Database Migrations

```bash
  docker compose exec web python manage.py migrate
```

---

## Create Superuser

```bash
  docker compose exec web python manage.py createsuperuser
```

---

## Run Tests Using Docker

```bash
  docker compose exec web python manage.py test app_name.tests
```

---

## Stop Containers

```bash
  docker compose down
```

---

## Docker Services

| Service | Description |
|---|---|
| web | Django REST Framework API application |
| db | PostgreSQL database service |

---

# API Documentation

Swagger/OpenAPI documentation is available through:

```
GET /api/docs/
```

OpenAPI schema:

```
GET /api/schema/
```

---

# Authentication

The API uses JWT authentication.

After login, include the access token in protected requests:

```
Authorization: Bearer <access_token>
```

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register/` | Register employee account |
| POST | `/api/login/` | Login and generate JWT tokens |
| POST | `/api/admin/create-manager/` | Create manager account (Superuser only) |

---

# Department Management

Departments are used to categorize employees.

Employees can only retrieve department information.

Department creation, updates, and deletion are managed by authorized users.

Base URL:

```
/api/departments/
```

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | List all departments |
| POST | `/` | Create department |
| GET | `/{public_id}/` | Retrieve department |
| PATCH | `/{public_id}/` | Update department |
| DELETE | `/{public_id}/` | Delete department |

---

# Employee Leave Management

Base URL:

```
/api/leave/employee/leave-requests/
```

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | View employee leave requests |
| POST | `/` | Apply for leave |
| GET | `/{public_id}/` | View specific leave request |
| PATCH | `/{public_id}/` | Update pending leave request |
| DELETE | `/{public_id}/` | Delete pending leave request |

---

# Manager Leave Management

Base URL:

```
/api/leave/manager/leave-requests/
```

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | View all leave requests |
| GET | `/{public_id}/` | View specific leave request |
| PATCH | `/{public_id}/approve/` | Approve leave request |
| PATCH | `/{public_id}/reject/` | Reject leave request |

---

# Filtering and Searching

## Employee Filters

Employees can filter their leave requests:

```
GET /api/leave/employee/leave-requests/?status=PENDING
```

Available filters:

- status
- leave_type


Examples:

```
GET /api/leave/employee/leave-requests/?leave_type=SICK
```

```
GET /api/leave/employee/leave-requests/?leave_type=SICK&status=PENDING
```

---

## Manager Filters

Managers can filter:

- Leave type
- Status

Examples:

```
GET /api/leave/manager/leave-requests/?status=APPROVED
```

```
GET /api/leave/manager/leave-requests/?leave_type=SICK
```

```
GET /api/leave/manager/leave-requests/?status=APPROVED&leave_type=SICK
```

Search employee by name:

```
GET /api/leave/manager/leave-requests/?search=John
```

---

# Testing

The project includes API integration tests covering:

- Authentication flow.
- Employee leave creation.
- Employee leave access restrictions.
- Leave update and deletion rules.
- Manager leave listing.
- Manager approval and rejection workflow.
- Filtering functionality.

Run tests:

```bash
  python manage.py test app_name.tests
```

---

# Assumptions

The following assumptions were made during implementation:

- User names are stored as first name, middle name, and last name fields instead of a single name field to provide better data structure and search capability.

- Departments are created and managed separately from user registration. Employees are assigned to existing departments.

- Email is used as the unique authentication identifier instead of username.

- Managers are created without department assignment, while employees are associated with departments.

- Each user has only one role: Employee or Manager.

- Django Superusers can only create manager accounts.

- Public UUID identifiers are used for API resource lookup instead of exposing database primary keys.

- Leave types are restricted to Sick, Casual, and Paid.

- Leave requests are soft deleted instead of permanently removed from the database.

---

# Technical Design Choices

- A custom user model using `AbstractBaseUser` with a custom user manager is used to provide control over authentication and user creation.

- Django REST Framework ViewSets are used for resource-based APIs.

- ReadOnlyModelViewSet is used for manager leave listing because approval and rejection are handled through dedicated custom actions.

- APIView is used for Login endpoint where custom request and response handling is required.

- drf-spectacular is used for Swagger/OpenAPI documentation.

---

# Project Structure

```
EmployeeLeaveManagement/
│
├── users/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── permissions.py
│   │   └── urls.py
│   │
│   ├── tests/
│   ├── managers.py
│   ├── models.py
│   └── ...
│
├── leave/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── permissions.py
│   │   ├── paginations.py
│   │   └── urls.py
│   │
│   ├── tests/
│   ├── models.py
│   └── ...
│
├── leave_management/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── manage.py
└── README.md
```