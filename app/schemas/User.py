from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    Name : str = Field(..., examples=["Robin hut"])
    PhoneNumber : str = Field(...,min_length=10, max_length=10, examples=[6294123456])
    Age : int = Field(...,ge=18, examples=["18"])
    Address : str | None = Field(None, examples=["Kolkata/WB"])
    is_active : bool = Field(..., examples=["Active/deactive"])
    
    
class UserShow(BaseModel):
    Name : str = Field(..., examples=["Robin hut"])
    PhoneNumber : int = Field(..., examples=[6294123456])
    age : int = Field(..., examples=["18+"])


class AddUserAddress(BaseModel):
    Address : str = Field(..., examples=["Kolkata/WB"])