# Flask Productivity API (JWT Auth Backend)

A secure Flask REST API for a productivity application that allows users to register, login, and manage personal notes. Each user can only access their own data, ensuring full authentication and authorization using JWT.

---

## Features

- User Registration & Login (JWT Authentication)
- Password hashing using Flask-Bcrypt
- Protected routes using JWT
- User-specific Notes resource (CRUD)
- Pagination for notes listing
- Secure access control (users cannot access others' data)
- RESTful API design

---

## Tech Stack

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- Marshmallow

---

## Project Structure

```text
flask-c10-summative-lab-sessions-and-jwt-clients/
│
├── Pipfile
├── Pipfile.lock
├── README.md
│
├── app.py              # Main application file (routes + app setup)
├── models.py           # Database models (User, Note)
├── config.py           # App configuration (DB, JWT settings)
├── seed.py             # Seeds database with fake data using Faker
│
├── migrations/         # Database migrations (Flask-Migrate)
│
├── client-with-jwt/    # Frontend (JWT authentication)
│
└── client-with-sessions/  # Frontend (Session authentication)
```

---

## Installation Setup

```bash
git clone https://github.com/madoyakimberley/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients
```

```bash
pipenv install
pipenv shell
```

---

## Database Setup

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

---

## Seed Database

```bash
python seed.py
```

---

## Run App

```bash
python app.py
```

App runs at:
http://127.0.0.1:5000

---

## Auth Flow

POST /signup  
POST /login  
GET /me (Bearer token required)

---

## Notes Endpoints

POST /notes  
GET /notes?page=1  
PATCH /notes/<id>  
DELETE /notes/<id>

---

## Security

- bcrypt password hashing
- JWT protected routes
- user isolation enforced
- proper HTTP status codes

---

## Pagination

GET /notes?page=1

Returns:

- notes
- page
- total_pages

---

## Author

Kimberley Madoya
