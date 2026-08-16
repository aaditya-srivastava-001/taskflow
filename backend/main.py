from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, get_db
import models
import schemas
import algorithms

from middleware import RequestTimingMiddleware


# =========================
# DATABASE
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="TaskFlow API",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REQUEST TIMING MIDDLEWARE
# =========================

app.add_middleware(
    RequestTimingMiddleware
)


# =========================
# ROOT / HEALTH
# =========================

@app.get("/")
def root():
    return {
        "message": "TaskFlow API is running"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "database": "connected"
    }


# =========================
# USERS
# =========================

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=201
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# =========================
# PROJECTS
# =========================

@app.post(
    "/projects",
    response_model=schemas.ProjectResponse,
    status_code=201
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    owner = (
        db.query(models.User)
        .filter(models.User.id == project.owner_id)
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse]
)
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


# =========================
# PROJECT STATISTICS
# =========================

@app.get("/projects/statistics")
def project_statistics(db: Session = Depends(get_db)):

    statistics = (
        db.query(
            models.Project.id.label("project_id"),
            models.Project.name.label("project_name"),

            func.count(models.Task.id).label("task_count"),

            func.sum(
                case(
                    (models.Task.status == "todo", 1),
                    else_=0
                )
            ).label("todo"),

            func.sum(
                case(
                    (models.Task.status == "in_progress", 1),
                    else_=0
                )
            ).label("in_progress"),

            func.sum(
                case(
                    (models.Task.status == "done", 1),
                    else_=0
                )
            ).label("done")
        )
        .outerjoin(
            models.Task,
            models.Project.id == models.Task.project_id
        )
        .group_by(
            models.Project.id,
            models.Project.name
        )
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "task_count": row.task_count,
            "todo": row.todo or 0,
            "in_progress": row.in_progress or 0,
            "done": row.done or 0
        }
        for row in statistics
    ]


# =========================
# TASKS
# =========================

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=201
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == task.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        due_date=task.due_date,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# =========================
# GET TASKS + FILTERING
# =========================

@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    project_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    if status is not None:
        query = query.filter(models.Task.status == status)

    if priority is not None:
        query = query.filter(models.Task.priority == priority)

    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)

    return query.all()


# =========================
# INSERTION SORT
# =========================

@app.get("/tasks/sorted")
def get_sorted_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(models.Task).all()

    sorted_tasks = algorithms.insertion_sort_tasks(tasks)

    return [
        {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
            "project_id": task.project_id
        }
        for task in sorted_tasks
    ]


# =========================
# LINEAR SEARCH
# =========================

@app.get("/tasks/search/linear")
def linear_search(
    title: str,
    db: Session = Depends(get_db)
):
    tasks = db.query(models.Task).all()

    task = algorithms.linear_search_tasks(
        tasks,
        title
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "algorithm": "Linear Search",
        "time_complexity": "O(n)",
        "task": {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
            "project_id": task.project_id
        }
    }


# =========================
# BINARY SEARCH
# =========================

@app.get("/tasks/search/binary")
def binary_search(
    title: str,
    db: Session = Depends(get_db)
):
    tasks = db.query(models.Task).all()

    task = algorithms.binary_search_tasks(
        tasks,
        title
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "algorithm": "Binary Search",
        "time_complexity": "O(log n) search after sorting",
        "task": {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
            "project_id": task.project_id
        }
    }


# =========================
# GET SINGLE TASK
# =========================

@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =========================
# UPDATE TASK
# =========================

@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    if "project_id" in update_data:

        project = (
            db.query(models.Project)
            .filter(
                models.Project.id ==
                update_data["project_id"]
            )
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

    if "priority" in update_data:

        if update_data["priority"] not in {
            "low",
            "medium",
            "high"
        }:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Priority must be "
                    "low, medium, or high"
                )
            )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


# =========================
# DELETE TASK
# =========================

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }