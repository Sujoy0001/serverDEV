import os
from typing import Optional
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from pydantic import BaseModel
from itsdangerous import Signer, BadSignature

router = APIRouter()


# 1. Cryptographic Signer Configuration
# In production, load this from an environment variable (e.g., os.getenv("SESSION_SECRET"))
SESSION_SECRET = "super-secret-high-entropy-crypto-key-123456!"
signer = Signer(SESSION_SECRET)

COOKIE_NAME = "secure_sid"

# 2. Mock Databases (In production, replace with Redis or PostgreSQL)
# Maps Session ID -> User Session Data
SESSION_STORE = {} 

# Maps Email -> User Object
USER_DB = {
    "user@domain.com": {
        "id": "usr_99X2",
        "email": "user@domain.com",
        "password_hash": "mocked_secure_password_hash" # Use passlib/bcrypt to verify in real apps
    }
}

# 3. Request Schemas
class LoginRequest(BaseModel):
    email: str
    password: str

# 4. Authentication Dependency (Session Verification)
def get_current_user(request: Request) -> dict:
    """
    Extracts, unsigns, and verifies the session cookie.
    Returns the session data if valid, otherwise raises a 401.
    """
    # Extract the cookie from the incoming request
    signed_sid = request.cookies.get(COOKIE_NAME)
    if not signed_sid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Active session cookie missing."
        )
    
    try:
        # Cryptographically verify the cookie hasn't been tampered with
        session_id = signer.unsign(signed_sid).decode("utf-8")
    except BadSignature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token signature."
        )
    
    # Lookup the session ID in the server-side store
    session_data = SESSION_STORE.get(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired or does not exist."
        )
        
    return session_data

# 5. Login Endpoint (Session Creation)
@router.post("/api/auth/login")
async def login(payload: LoginRequest, response: Response):
    user = USER_DB.get(payload.email)
    
    # Validate credentials (In reality, use pwd_context.verify(payload.password, user['password_hash']))
    if not user or payload.password != "password123": 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Generate a secure, random Session ID
    import os
    import secrets
    session_id = secrets.token_hex(32)
    
    # Store user state on the server side
    SESSION_STORE[session_id] = {
        "user_id": user["id"],
        "email": user["email"]
    }
    
    # Cryptographically sign the session ID before sending it to the client
    signed_sid = signer.sign(session_id.encode("utf-8")).decode("utf-8")
    
    # Set the secure cookie in the HTTP response
    response.set_cookie(
        key=COOKIE_NAME,
        value=signed_sid,
        httponly=True,        # Prevents XSS scripts from accessing the cookie
        secure=True,          # Enforces HTTPS (Set to False ONLY during local development/HTTP)
        samesite="lax",       # Mitigates CSRF vulnerabilities
        max_age=7200,         # Automatic session expiration window in seconds (2 hours)
        httponly_override=True # Enforces browser level cookie locking
    )
    
    return {"message": "Successfully logged in"}

# 6. Protected Endpoint
@router.get("/api/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    # If control reaches here, the session is fully verified
    return {
        "secret_data": "Confidential corporate metrics",
        "user_email": current_user["email"]
    }

# 7. Logout Endpoint (Session Invalidation)
@router.post("/api/auth/logout")
async def logout(request: Request, response: Response):
    signed_sid = request.cookies.get(COOKIE_NAME)
    
    if signed_sid:
        try:
            # Safely extract the server-side ID to remove it
            session_id = signer.unsign(signed_sid).decode("utf-8")
            SESSION_STORE.pop(session_id, None) # Evict from server cache
        except BadSignature:
            pass # Ignore invalid signatures on logout and proceed with deletion
            
    # Command the browser to clear the client-side cookie immediately
    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return {"message": "Successfully logged out"}
