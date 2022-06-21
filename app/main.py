from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='root', cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
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
def get_posts(db: Session = Depends(get_db)):
    # sql = 'SELECT * FROM posts'
    # cursor.execute(sql)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {
        "data": posts
    }


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # sql = "SELECT * FROM posts WHERE id = %s"
    # cursor.execute(sql, (str(id), ))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = db.query(models.Post).filter(models.Post.id == id).one_or_none()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "message": f"post with id: {id} was not found"
        # }

    return {
        "data": post
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: dict = Body(...)):
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # sql = "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"
    # cursor.execute(sql, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {
        "data": new_post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting post
    # sql = "DELETE FROM posts WHERE id = %s RETURNING *"
    # cursor.execute(sql, (str(id), ))
    # deletedPost = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # sql = "UPDATE posts SET title = %s, content =  %s, published = %s WHERE id = %s RETURNING *"
    # cursor.execute(sql, (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    dbPost = post_query.first()

    if dbPost == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_query.update(post_dict)
    
    db.commit()

    return {
        "data": post_query.first()
    }