
from os import stat
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # What OAuth2PasswordRequestForm returns
    # username =
    # password =
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    # user = db.query(models.User).filter(
    #     models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data={
        "user_id": user.id
    })
    # return token

    return {
        "access_token":  access_token,
        "token_type": "bearer"
    }
