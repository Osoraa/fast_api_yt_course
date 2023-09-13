from fastapi import FastAPI

app = FastAPI()


# Root route
@app.get("/")
def root():
    return {"message": "Hello World from FastApi"}


# Get Posts endpoint
@app.get("/posts")
def get_posts():
    return {"data": "Empty posts"}
