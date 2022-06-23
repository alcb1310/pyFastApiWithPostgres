from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World!!", "success": True}