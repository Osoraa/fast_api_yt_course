from fastapi import FastAPI

app = FastAPI()


# Root route
@app.get("/")
def root():
    return {"message": "Hello World from FastApi"}
