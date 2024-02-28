# Internet_Portal_Back_end

Стек: FastAPI, Pydantic, Starlette, PostgreSQL, JWT, Uvicorn


python3 -m venv venv   
 source venv/bin/activate 

pip install --upgrade pip
pip install fastapi

pip install unicorn
pip install 


Run:

    uvicorn main:app --reload

Interactive API docs:

    http://127.0.0.1:8000/docs#/







поднять контейнер с БД:
    
        - docker compose up -d
    
        - docker compose exec db psql Internet_Portal_DB --username Internet_Portal --password
