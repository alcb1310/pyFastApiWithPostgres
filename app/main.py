from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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

while True:
    try:
        conn = psycopg2.connect(host='localhost', database = 'fastapi', user='postgres' , password = 'root', cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print ("Connecting to database failed")
        print ("Error: ", error)
        time.sleep(2)

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
    sql = 'SELECT * FROM posts'
    cursor.execute(sql)
    posts = cursor.fetchall()
    return {
        "data": posts
    }

# @app.get('/posts/latest')
# def get_latest_post():
#     post = my_posts[len(my_posts) -1]
#     return {
#         "data": post
        
#     }

@app.get("/posts/{id}")
def get_post(id: int):
    sql = "SELECT * FROM posts WHERE id = %s"
    cursor.execute(sql, (str(id), ))
    
    post = cursor.fetchone()

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
    sql = "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"
    cursor.execute(sql, (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "data": new_post
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    sql = "DELETE FROM posts WHERE id = %s RETURNING *"
    cursor.execute(sql, (str(id), ))
    deletedPost = cursor.fetchone()
    if deletedPost == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    sql = "UPDATE posts SET title = %s, content =  %s, published = %s WHERE id = %s RETURNING *"
    cursor.execute(sql, (post.title, post.content, post.published, str(id)))
    
    updatedPost = cursor.fetchone()
    if updatedPost == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
        
    conn.commit()
    # index = find_post_index(id)
    
    # if index == None:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist")
    
    # post_dict = post.dict()
    
    # post_dict['id']= id
    # my_posts[index] = post_dict
    
    return {
        "data": updatedPost
    }