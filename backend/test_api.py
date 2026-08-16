from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


# =========================
# HEALTH
# =========================

def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "connected"


# =========================
# ROOT
# =========================

def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "TaskFlow API is running"


# =========================
# GET USERS
# =========================

def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =========================
# GET PROJECTS
# =========================

def test_get_projects():
    response = client.get("/projects")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =========================
# GET TASKS
# =========================

def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =========================
# TASK FILTERING
# =========================

def test_task_filter_status():
    response = client.get(
        "/tasks",
        params={"status": "todo"}
    )

    assert response.status_code == 200

    tasks = response.json()

    for task in tasks:
        assert task["status"] == "todo"


def test_task_filter_priority():
    response = client.get(
        "/tasks",
        params={"priority": "high"}
    )

    assert response.status_code == 200

    tasks = response.json()

    for task in tasks:
        assert task["priority"] == "high"


# =========================
# STATISTICS
# =========================

def test_project_statistics():
    response = client.get(
        "/projects/statistics"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =========================
# ALGORITHM ENDPOINTS
# =========================

def test_sorted_tasks():
    response = client.get("/tasks/sorted")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_linear_search_not_found():
    response = client.get(
        "/tasks/search/linear",
        params={"title": "Definitely Not A Real Task"}
    )

    assert response.status_code == 404


def test_binary_search_not_found():
    response = client.get(
        "/tasks/search/binary",
        params={"title": "Definitely Not A Real Task"}
    )

    assert response.status_code == 404