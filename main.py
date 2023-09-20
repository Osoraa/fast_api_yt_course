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
    publish: bool = True
    location: Optional[str] = None


posts = [
    {
        'title': 'Second post in Postman',
        'content': 'Testing Optionals and Defaults',
        'publish': True,
        'location': None,
        'id': 92
    },
    {
        'title': 'Placeholder post',
        'content': 'Basic Defaults',
        'publish': False,
        'location': "Lagos",
        'id': 90
    }
]


def find_post(id=int) -> dict:
    """Retrieve post"""

    for post in posts:
        if post["id"] == id:
            return post


@app.get("/")
def root():
    """Root route"""

    return {"message": "Hello World from FastApi"}


@app.get("/posts")
def get_posts():
    """Get Posts endpoint"""

    return {"data": posts}


@app.post("/posts")
def create_post(body: dict = Body(...)):
    """First post request"""

    print(body)
    return {"msg": f"Successfully created post with title {body['Title']}"}


@app.post("/create_post_2")
def create_post_2(body: Post):
    """Second post request"""

    data = dict(body)

    # Use the UUID package for the post ID
    data["id"] = uuid4().time
    posts.append(data)
    print(data)

    return {"msg": f"Successfully created post2 with title {body.title}"}


@app.get("/posts/{id}")
def get_post(id: int):
    """Route to get a single Post"""

    post = find_post(id)
    print(post)

    return {"data": post}
