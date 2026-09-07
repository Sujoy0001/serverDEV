import uuid
from app.schemas.User import UserCreate, AddUserAddress

# The source of truth for your data
UserDB = {}

def get_user_by_name(name: str) -> dict | None:
    """Find a user by name."""
    for user in UserDB.values():
        if user["name"] == name:
            return user
    return None

def get_user_by_id(user_id: str) -> dict | None:
    """Find a user by their UUID."""
    return UserDB.get(user_id)

def create_user(user_data: UserCreate) -> dict:
    """Generate an ID and save a new user."""
    user_id = str(uuid.uuid4())
    
    # FIX: Inject the generated ID into the dictionary so response_model handles it
    new_user = {
        "id": user_id,
        **user_data.model_dump()
    }
    
    UserDB[user_id] = new_user
    return new_user

def update_user_address(user_id: str, address_data: AddUserAddress) -> dict | None:
    """Update only the address field of a user."""
    if user_id in UserDB:
        # FIX: Lowercase 'address' to match the schema design definition
        UserDB[user_id]["address"] = address_data.Address
        return UserDB[user_id]
    return None

def delete_user(user_id: str) -> bool:
    """Remove a user from the database."""
    if user_id in UserDB:
        del UserDB[user_id]
        return True
    return False

def show_all_users() -> list[dict]:
    """Return a list of all registered users in the database."""
    return list(UserDB.values())
