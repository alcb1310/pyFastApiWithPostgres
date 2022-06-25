
### create a virtual environment  
#### venv => where the virtual environment is intalled
```
pip install virtualenv
virtualenv venv
```

### activate virtual environment
```
source ./venv/bin/activate
```

### Install all packages 
```
pip install -r requirements.txt
```


### Start the server
```
uvicorn app.main:app --reload
```

### Upgrading the database
```
heroku run alembic upgrade head
```