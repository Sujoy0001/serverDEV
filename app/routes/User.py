from fastapi import APIRouter, HTTPException, status
from app.schemas.User import UserCreate, UserShow, AddUserAddress
from app.curd.user import create_user, get_user_by_name, get_user_by_id, update_user_address, delete_user, show_all_users

router = APIRouter(prefix="/users", tags=["Users"])

# 1. CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserShow)
def user_create_route(user: UserCreate):
    if get_user_by_name(user.Name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with name '{user.Name}' already exists."
        )
    return create_user(user)

# 2. READ (Get single user by UUID)
@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserShow)
def user_get_route(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user

# 3. UPDATE (Patch address)
@router.patch("/{user_id}/address", status_code=status.HTTP_200_OK)
def user_update_address_route(user_id: str, address_data: AddUserAddress):
    updated_user = update_user_address(user_id, address_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return {"message": "Address updated successfully", "address": updated_user["address"]}

# 4. DELETE
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def user_delete_route(user_id: str):
    success = delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    # HTTP 204 requires returning no body content
    return None

@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[UserShow])
def list_all_users_route():
    """Retrieve all registered users as a list."""
    return show_all_users()