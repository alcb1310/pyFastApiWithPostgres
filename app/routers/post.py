from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter()


@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # sql = 'SELECT * FROM posts'
    # cursor.execute(sql)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.get("/posts/{id}", response_model=schemas.PostResponse)
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

    return post


@router.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
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

    return new_post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/posts/{id}", response_model=schemas.PostResponse)
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

    return post_query.first()