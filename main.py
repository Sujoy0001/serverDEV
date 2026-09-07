from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class Name(BaseModel):
    name : str = Field(..., examples=["sujoy"])

@app.get("/")
def read_root():
    return {"Message": "Backend Engineering Fundamentals"}

userDB = ["sujoy", "sudip", "sanjoy"]

@app.get("/all", status_code=status.HTTP_200_OK)
def show_all_elements():
    if None in userDB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='List is Empty'
        )
    
    return userDB

@app.post("/add", status_code=status.HTTP_201_CREATED)
def add_value(user: Name) -> dict[str, str]:
    if user in userDB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user} already in db"
        )
        
    userDB.append(user.name)
    
    return {"message": f"{user.name} is added to db"}