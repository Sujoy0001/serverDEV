from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import uuid

router = APIRouter()

# Schems
class Books(BaseModel):
    BookName : str = Field(...)
    AuthorName : str = Field(..., description='Right the author name')
    Descriptions : str | None = Field(None, description='Description not write')
    Is_available : bool 
    
class AddBook(BaseModel):
    bookname : str
    Authorname : str
    descriptions : str | None
    
class ShowBook(BaseModel):
    BookName : str
    AuthorName : str
    Descriptions : str

class ShowBookById(BaseModel):
    book_id : str = Field(...)
    
Library = {}

# logic

def getBookName(name):
    return any(book["BookName"].lower() == name.lower() for book in Library.values())

# CURD oprations

# routes 

@router.get("/books", response_model=dict[str, ShowBook], status_code=status.HTTP_200_OK)
def AllBooks():
    if not Library:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='The Library is empty'
        )
        
    return Library

@router.post("/books", status_code=status.HTTP_201_CREATED)
def AddBooks(book : AddBook):
    
    if getBookName(book.bookname):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{book.bookname} is already exits'
        )
        
    book_id = str(uuid.uuid4())
    
    Library[book_id] = {
        "BookName" : book.bookname,
        "AuthorName" : book.Authorname,
        "Descriptions" : book.descriptions,
        "Is_available" : True
    }
    
    return f'Book id {book_id} | Book name {book.bookname} is add to Library'

@router.post("/books/{id}", response_model=ShowBook, status_code=status.HTTP_200_OK)
def BookShowById(id : ShowBookById):
    
    if id in Library:
        return Library[id]
    else:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f'book id {id} not Found'
        )