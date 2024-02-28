from databases import Database
import uvicorn
from typing import Union

from fastapi import FastAPI
from routers.permissions import permission_router
from routers.roles import role_router
from routers.calendar import calendar
from routers.user import routes
from routers.profile import profile
from routers.feedback import feedback
from routers.job_application import job_application_router
from routers.departments import departments_router

app = FastAPI()

app.include_router(routes)
app.include_router(profile)
app.include_router(feedback)
app.include_router(calendar)
app.include_router(permission_router)
app.include_router(role_router)
app.include_router(job_application_router)
app.include_router(departments_router)
# @app.get("/hello/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True, workers=3)
