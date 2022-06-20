from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

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


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

    return {
        "message": "not found"
    }


@app.get("/")
def root():
    return {"message": "Hello World!!", "success": True}


@app.get("/posts")
def get_posts():
    return {
        "data": my_posts
    }

@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts) -1]
    return {
        "data": post
        
    }

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {
        "data": post
    }

@app.post("/posts")
# def create_posts(payload: dict = Body(...)):
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000000)
    my_posts.append(post_dict)
    return {
        "data": post_dict
    }
