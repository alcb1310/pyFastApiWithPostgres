from fastapi import Body, FastAPI

app = FastAPI()

# Order matters, first written is what serves


@app.get("/")
def root():
    return {"message": "Hello World!!", "success": True}


@app.get("/posts")
def get_posts():
    return {
        "data": "This is your post"
    }


@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    # print(payload)
    return {
        "message": "succesfully created post",
        "new_post": {
            "title": payload['title'],
            "content": payload['content']
        }
    }
