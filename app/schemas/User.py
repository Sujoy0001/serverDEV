from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    Name : str = Field(..., examples=["Robin hut"])
    PhoneNumber : str = Field(...,min_length=10, max_length=10, examples=["6294123456"])
    Age : int = Field(...,ge=18, examples=[17])
    Address : str | None = Field(None, examples=["Kolkata/WB"])
    is_active : bool = Field(..., examples=[True])
    
    
class UserShow(BaseModel):
    id : str = Field(..., examples=['54dg45f44-454f5d545f4s-d4f5f4d54d-547f47df5'])
    Name : str = Field(..., examples=["Robin hut"])
    PhoneNumber : int = Field(..., examples=["6294123456"])
    age : int = Field(..., examples=[17])


class AddUserAddress(BaseModel):
    Address : str = Field(..., examples=["Kolkata/WB"])