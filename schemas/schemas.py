from typing import List
from pydantic import BaseModel
from datetime import datetime


class UserSchemas(BaseModel):
    id: int
    email: str
    created_at: datetime
    updated_at: datetime
    is_verified: bool
    hashed_password: str
    is_active: bool
    is_superuser: bool
    role_id: int


class UpdateUser(BaseModel):
    email: str
    is_verified: bool
    is_active: bool
    is_superuser: bool
    role_id: int


class ConfirmationCodeSchemas(BaseModel):
    id: int
    user_id: int
    code: int
    created_at: datetime
    updated_at: datetime


class PersonalInfoSchemas(BaseModel):
    id: int
    user_id: int
    name: str
    surname: str
    patronymic: str
    position_id: int
    job_title_id: int
    city: str


class PersonalInfoUpdate(PersonalInfoSchemas):
    pass


class Role(BaseModel):
    id: int
    role_name: str


class Permission(BaseModel):
    id: int
    permission_type: str


class RoleSchemas(BaseModel):
    role_name: str
    

class UserProjects(BaseModel):
    id: int
    user_id: int
    project_id: int
    created_at: datetime
    updated_at: datetime


class Project(BaseModel):
    id: int
    project_name: str
    created_at: datetime
    updated_at: datetime


class JobTitle(BaseModel):
    id: int
    job_title_name: str


class Position(BaseModel):
    id: int
    position_name: str


class UserFeedbackSchemas(BaseModel):
    user_feedbacks_id: int
    user_created_id: int
    description: str
    created_at: datetime


class UserCalendarSchemas(BaseModel):
    id: int
    user_id: int


class TaskOnTheCalendarSchemas(BaseModel):
    user_calendar_id: int
    user_created_id: int
    task_name: str
    description: str
    date_time_start: datetime
    date_time_end: datetime
    created_at: datetime


class TaskOnTheCalendarSchemasUpdate(BaseModel):
    task_name: str
    description: str
    date_time_start: datetime
    date_time_end: datetime

class JobApplicationSchemas(BaseModel):
    user_id: int
    department_id: int
    status_id: int
    #file_busket_id: (ForeignKey("files.id"))
    trouble_shooter_id: int
    title: str
    description: str
    priority: int
    created_at: datetime
    updated_at: datetime

class JobApplicationAnswerSchemas(BaseModel):

    job_application_id: int
    user_created_id: int
    department_id: int
    created_at: datetime
    priority: int
    status_id: str
    #file_busket_id: (ForeignKey("files.id"))

class UserLeaderships(BaseModel):
   
    user_id: int
    is_subordianated_user_id: int
    is_chef_user_id: int
    name_chef_position: str