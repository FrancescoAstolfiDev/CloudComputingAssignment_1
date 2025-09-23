from typing import Dict

from fastapi import FastAPI, HTTPException
from .config import settings
from .model import UserInDB
from .validator import UserValidator
from .schemas import UserNoAlias,UserUpdate

app = FastAPI(title=settings.app_name)


@app.get("/")
async def root():
    return {"message": "User DB Service"}


@app.post("/db_user", response_model=UserNoAlias, summary="Insert a user into the database")
async def write_user(user: UserNoAlias):
    """
    Receives a fully-formed UserInDB instance and inserts it into the database
    without additional validation.
    """

    validator = UserValidator.get_instance()
    try:
        user=validator.insert_user(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.put("/db_user", response_model=Dict[str,int], summary="Update a user in the database")
async def update_user(user: UserUpdate):
    validator = UserValidator.get_instance()
    print(user)
    try:
        file_changed = validator.edit_user(user)
        return {"modified_count":file_changed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



@app.get("/db_user", response_model=UserNoAlias, summary="Get a user by user_id or email")
async def get_user(identifier: str):
    """
    Retrieve a user by identifier, which can be either:
    - a 7-character user_id
    - a valid email
    """
    validator = UserValidator.get_instance()
    try:
        user = validator.get_user(identifier)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/db_user/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}

