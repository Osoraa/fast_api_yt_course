from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI()

class Post(BaseModel):
    """Base Post class"""

    title: str
    content: str
    publish: bool=True
    location: Optional[str]=None
    
posts = []


# Root route
@app.get("/")
def root():
    return {"message": "Hello World from FastApi"}


# Get Posts endpoint
@app.get("/posts")
def get_posts():
    return {"data": posts}


# First post request
@app.post("/posts")
def create_post(body: dict=Body(...)):
    print(body)
    return {"msg": f"Successfully created post with title {body['Title']}"}


# Second post request
@app.post("/create_post_2")
def create_post_2(body: Post):
    body = dict(body)
    
    # Use the UUID package for the post ID
    body["id"] = uuid4().time
    posts.append(body)
    print(posts[0])
    
    return {"msg": f"Successfully created post2 with title {body['title']}"}