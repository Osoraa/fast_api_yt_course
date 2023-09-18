from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    
    
# Root route
@app.get("/")
def root():
    return {"message": "Hello World from FastApi"}


# Get Posts endpoint
@app.get("/posts")
def get_posts():
    return {"data": "Empty posts"}


# First post request
@app.post("/create_post")
def create_post(body: dict = Body(...)):
    print(body)
    return {"msg": f"Successfully created post with title {body['Title']}"}


# Second post request
@app.post("/create_post_2")
def create_post(body:Post):
    print(body)
    return {"msg": f"Successfully created post2 with title {body.title}"}