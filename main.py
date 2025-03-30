from fastapi import FastAPI
from src.api import contacts
from src.repository.database.db import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(contacts.router)
