from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }


class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = {
        "from_attributes": True
    }


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "todo"
    due_date: Optional[date] = None
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        allowed = {"low", "medium", "high"}

        if value not in allowed:
            raise ValueError("Priority must be low, medium, or high")

        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None
    project_id: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    due_date: Optional[date]
    project_id: int

    model_config = {
        "from_attributes": True
    }
    