from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep


app = FastAPI()


# Post Class
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
            "dbname=fastapi user=postgres port=5433 password=postgres", cursor_factory=RealDictCursor)

        cur = conn.cursor()

        print("Database connected successfully!!")
        break

    except Exception as error:
        print("Error - ", error)
        sleep(2)


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


# Retrieves all posts in database
@app.get("/posts")
def get_posts() -> dict:
    """Get Posts endpoint"""

    cur.execute("""SELECT * FROM posts""")

    posts = cur.fetchall()

    return {"data": posts}


# Creates and appends post to Posts dict
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(body: Post) -> dict:
    """Second post request"""

    cur.execute("""INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING * """,
                (body.title, body.content, body.publish))

    data = cur.fetchone()

    print(data)

    # Conmmit on the db connection object not cursor
    conn.commit()

    return {"msg": f"Successfully created post with title: {data['title']}"}


# Gets a single post
@app.get("/posts/{id}")
def get_post(id: int) -> dict:
    """Route to get a single Post"""

    post = posts[find_post_index(id)]

    print(post)

    return {"data": post}


# Deletes a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    """Delete a post"""

    print(f"\n{posts}\n")

    post = posts[find_post_index(id)]

    remove_post(post)

    print(f"\n{posts}\n")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updates an existing post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, body: Post) -> dict:
    """Update a Post"""

    index = find_post_index(id)

    data = dict(body)

    posts[index].update(data)

    return {"data": posts[index]}
