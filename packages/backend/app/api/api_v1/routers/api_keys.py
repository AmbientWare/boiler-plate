from fastapi import APIRouter, Depends
from typing import List

# project imports
from app.db.session import get_db
from app.db.models import Token
from app.core import security
from app.core.auth import get_current_active_user

api_key_router = r = APIRouter()


# create a new token for a user
@r.post("/tokens/new")
async def new_token(db=Depends(get_db), user=Depends(get_current_active_user)):
    """Generate token that will never expire"""
    permissions = user.role
    access_token = security.create_api_key(
        data={"sub": user.email, "permissions": permissions}, never_expire=True
    )

    # save the token to the database
    db_api_key = Token(user_id=user.id, hashed_token=access_token)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)

    return {"api_key": access_token}


# return the user's api tokens
@r.get("/tokens")
async def get_user_tokens(db=Depends(get_db), user=Depends(get_current_active_user)):
    """Get all the user's api keys"""
    hashed_tokens: List[Token] = db.query(Token).filter(Token.user_id == user.id).all()

    if not hashed_tokens:
        return []

    # use the security function to decode the token
    decoded_keys = [
        security.decode_api_key(str(key.hashed_key)) for key in hashed_tokens
    ]

    return decoded_keys
