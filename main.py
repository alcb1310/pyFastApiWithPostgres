from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

# Order matters, first written is what serves

# title: string
# content: string


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "id": 1,
        "title": "title of post 1",
        "content": "content of post 2"
    },
    {
        "id": 2,
        "title": "favorite foods",
        "content": "I like pizza"
    }
]


@app.get("/")
def root():
    return {"message": "Hello World!!", "success": True}


@app.get("/posts")
def get_posts():
    return {
        "data": my_posts
    }


@app.post("/posts")
# def create_posts(payload: dict = Body(...)):
def create_posts(post: Post):
    print(post)
    print(post.content)
    print(post.dict())
    return {
        "data": post
    }
