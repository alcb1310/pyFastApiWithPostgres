from operator import index
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


my_posts = [
    {
        "id": 1,
        "title": "title of post 1",
        "content": "content of post 1"
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
        
def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


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

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "message": f"post with id: {id} was not found"
        # }
    
    return {
        "data": post
    }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: dict = Body(...)):
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000000)
    my_posts.append(post_dict)
    return {
        "data": post_dict
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required id
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    # my_posts.pop(index)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
    post_dict = post.dict()
    
    post_dict['id']= id
    my_posts[index] = post_dict
    
    return {
        "data": post_dict
    }