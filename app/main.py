from enum import auto
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine, get_db
from typing import List
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='root', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World!!", "success": True}
