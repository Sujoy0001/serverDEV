from fastapi import FastAPI, HTTPException, status
from app.routes.User import router as user_routes

app = FastAPI()


UserDB = []


@app.get("/")
def read_root():
    return {"Message": "Backend Engineering Fundamentals"}


app.include_router(user_routes)