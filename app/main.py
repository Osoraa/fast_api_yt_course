from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep


app = FastAPI()


# Post Class
class Post(BaseModel):
    """Base Post class"""

    title: str
    content: str
    publish: bool = False
    # location: Optional[str] = None


# Connect to the posts table on the fastapi database
while True:
    try:
        conn = psycopg2.connect(
            "dbname=fastapi user=postgres port=5432 password=postgres", cursor_factory=RealDictCursor)

        cur = conn.cursor()

        print("Database connected successfully!!")
        break

    except Exception as error:
        print("Error - ", error)
        sleep(2)


# Default route - Landing page
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

    cur.execute("""INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING *""",
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

    # A tuple has to be passed to the query in cur.execute for it to work
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (id,))

    post = cur.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    print(post)

    return {"data": post}


# Deletes a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> Response:
    """Delete a post"""

    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))

    post = cur.fetchone()

    print(f"\n{post}\n")

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updates an existing post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, body: Post) -> dict:
    """Update a Post"""

    cur.execute("""UPDATE posts SET title=%s, content=%s, publish=%s WHERE id = %s RETURNING *""",
                (body.title, body.content, body.publish, id))

    post = cur.fetchone()

    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    conn.commit()

    return {"Updated post": post}
