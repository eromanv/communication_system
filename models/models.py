from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from schemas.schemas import UserCalendarSchemas

# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

user_calendar = Table(
    "user_calendars_many_to_many",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("task_on_calendar_id", Integer, ForeignKey("tasks_on_calendar.id")),
)

user_feedbacks = Table(
    "user_feedbacks",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("user_feedback_id", Integer, ForeignKey("user_feedback.id")),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    hashed_password = Column(String(500))
    is_active = Column(Boolean)
    is_superuser = Column(Boolean, default=False)
    role_id = Column(
        Integer, ForeignKey("roles.id")
    )  # Этот столбец указывает роль пользователя

    tasks_on_calendar_users = relationship(
        "TaskOnTheCalendar", secondary=user_calendar, back_populates="users"
    )
    user_feedbacks = relationship(
        "UserFeedback", secondary=user_feedbacks, back_populates="users"
    )
    role = relationship("Role", back_populates="users")  # Связь с ролью пользователя


class ConfirmationCode(Base):
    __tablename__ = "confirmation_codes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    code = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class PersonalInfo(Base):
    __tablename__ = "personal_info"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    surname = Column(String(100))
    patronymic = Column(String(100))
    position_id = Column(Integer, ForeignKey("positions.id"))
    job_title_id = Column(Integer, ForeignKey("job_titles.id"))
    city = Column(String(100))


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(100))

    users = relationship("User", back_populates="role")
    permissions = relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )


class UserProject(Base):
    __tablename__ = "user_projects"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    project_name = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class JobTitle(Base):
    __tablename__ = "job_titles"

    id = Column(Integer, primary_key=True)
    job_title_name = Column(String(100))


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    position_name = Column(String(100))


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_feedbacks_id = Column(Integer)
    user_created_id = Column(Integer, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())

    users = relationship(
        "User", secondary=user_feedbacks, back_populates="user_feedbacks"
    )


# class UserFeedbacks(Base):
#     __tablename__ = "user_feedbacks"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))

# class UserCalendar(Base):
#     __tablename__ = 'user_calendars'

#     id = Column(Integer, primary_key=True, index=True)

#     users = relationship("User", secondary=user_calendar, back_populates="calendars")


class TaskOnTheCalendar(Base):
    __tablename__ = "tasks_on_calendar"

    id = Column(Integer, primary_key=True, index=True)
    user_calendar_id = Column(Integer)
    user_created_id = Column(Integer, index=True)
    task_name = Column(String, index=True)
    description = Column(String)
    date_time_start = Column(DateTime)
    date_time_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow())
    users = relationship(
        "User", secondary=user_calendar, back_populates="tasks_on_calendar_users"
    )


class PermissionType(Enum):
    read = "read"
    write = "write"
    delete = "delete"
    # И другие права


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    permission_type = Column(SQLAlchemyEnum(PermissionType), nullable=False)

    roles = relationship(
        "Role", secondary="role_permissions", back_populates="permissions"
    )


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    department = Column(String)


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    department_id = Column(ForeignKey("departments.id"))
    status_id = Column(ForeignKey("status.id"))
    # file_busket_id = Column(ForeignKey("files.id"))
    trouble_shooter_id = Column(Integer)
    title = Column(String(50))
    description = Column(String(1000))
    priority = Column(Integer())
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)


class JobApplicationAnswer(Base):
    __tablename__ = "job_application_answer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_application_id = Column(ForeignKey("job_applications.id"))
    user_created_id = Column(String(50))
    department_id = Column(ForeignKey("departments.id"))
    created_at = Column(DateTime, default=datetime.utcnow())
    priority = Column(Integer())
    status_id = Column(ForeignKey("status.id"))
    # file_basket_id

class UserLeadership(Base):
    __tablename__ = 'user_leadership'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey('users.id'))
    is_subordinated_id = Column(Integer)
    is_head_id = Column(Integer)
    position_name = Column(String)