from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import psycopg2
from time import sleep


app = FastAPI()


class Post(BaseModel):
    """Base Post class"""

    title: str
    content: str
    publish: bool = True
    # location: Optional[str] = None


# Connect to the posts table on the fastapi database
while True:
    try:
        conn = psycopg2.connect(
            "dbname=fastapi user=postgres port=5433 password=postgres")

        cur = conn.cursor()

        cur.execute("SELECT * FROM posts")

        posts = cur.fetchall()

        print("Database connected successfully!!")
        break

    except Exception as error:
        print("Error - ", error)
        sleep(2)


# Posts database is a list of dicts
# posts = [
#     {
#         'title': 'Second post in Postman',
#         'content': 'Testing Optionals and Defaults',
#         'publish': True,
#         'location': None,
#         'id': 92
#     },
#     {
#         'title': 'Placeholder post',
#         'content': 'Basic Defaults',
#         'publish': False,
#         'location': "Lagos",
#         'id': 90
#     }
# ]


def find_post_index(id: int) -> int:
    """Retrieve post"""

    for post in posts:
        if post["id"] == id:
            return posts.index(post)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} does not exist")


def remove_post(post: dict) -> None:
    """Delete a post"""

    global posts

    posts = [p for p in posts if p != post]


@app.get("/")
def root():
    """Root route"""

    return {"message": "Hello World from FastApi"}


@app.get("/posts")
def get_posts() -> dict:
    """Get Posts endpoint"""

    return {"data": posts}


# Creates a post but doesn't append to Posts dict
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(body: dict = Body(...)) -> dict:
#     """First post request"""

#     print(body)
#     return {"msg": f"Successfully created post with title {body['title']}"}


# Creates and appends post to Posts dict
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post_2(body: Post) -> dict:
    """Second post request"""

    data = dict(body)

    # Use the UUID package for the post ID
    data["id"] = uuid4().time
    posts.append(data)
    print(data)

    return {"msg": f"Successfully created post2 with title {body.title}"}


@app.get("/posts/{id}")
def get_post(id: int) -> dict:
    """Route to get a single Post"""

    post = posts[find_post_index(id)]

    print(post)

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    """Delete a post"""

    print(f"\n{posts}\n")

    post = posts[find_post_index(id)]

    remove_post(post)

    print(f"\n{posts}\n")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, body: Post) -> dict:
    """Update a Post"""

    index = find_post_index(id)

    data = dict(body)

    posts[index].update(data)

    return {"data": posts[index]}
