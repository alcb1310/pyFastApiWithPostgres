# FastAPI tutorial

How to install and execute this app 

## Installation process

### create a virtual environment  

venv => where the virtual environment is intalled

```
pip install virtualenv
virtualenv venv
```

### activate virtual environment
```
source ./venv/bin/activate
```

## Installing all dependencies

### Install all packages 
```
pip install -r requirements.txt
```

## Runing the program locally

### Start the server
```
uvicorn app.main:app --reload
```

### Upgrading the database locally
```
alembic upgrade head
```

### Upgrading the database on heroku
```
heroku run alembic upgrade head
```

## Configuration needed

### Environment variables
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=