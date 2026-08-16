# TaskFlow

TaskFlow is a full-stack task management application built with a FastAPI
backend, SQLAlchemy ORM, SQLite database, and a lightweight HTML/CSS/JavaScript
frontend.

The project demonstrates REST API development, relational database design,
validation, filtering, SQL aggregation, middleware, CORS, automated testing,
and fundamental data structures and algorithms.

---

## Features

### Backend

- FastAPI REST API
- SQLAlchemy ORM
- SQLite database
- Pydantic validation
- User management
- Project management
- Task management
- Task CRUD operations
- Task filtering by status, priority, and project
- Project statistics
- SQL aggregation
- Request timing middleware
- CORS support
- HTTP error handling
- AI-style Quick-Add task creation
- Algorithm-based task sorting and searching

### Frontend

- Responsive HTML/CSS/JavaScript interface
- Task dashboard
- Task statistics
- Task creation
- Task editing
- Task deletion
- Task search
- Status filtering
- Priority filtering
- AI Quick-Add interface
- API integration using Fetch API
- Local browser caching using localStorage
- DOM-based task rendering

### Algorithms

TaskFlow implements:

- Insertion Sort
- Linear Search
- Binary Search

The project also includes:

- Comparison counting
- Algorithm benchmark testing
- Automated PASS/FAIL algorithm verification
- Multiple dataset sizes

---

## AI Quick-Add

TaskFlow includes a deterministic AI-style Quick-Add feature that allows users
to describe a task using natural language.

Example:

```text
Finish project report by Friday high priority

Technology Stack

Backend
Python 3.10
FastAPI
SQLAlchemy
Pydantic
SQLite
Uvicorn

Frontend
HTML5
CSS3
JavaScript
Fetch API
localStorage

Testing
Pytest
HTTPX
FastAPI TestClient