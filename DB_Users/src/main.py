from fastapi import FastAPI, HTTPException
from .config import settings
from .model import UserInDB
from .validator import UserValidator

app = FastAPI(title=settings.app_name)


@app.get("/")
async def root():
    return {"message": "User DB Service"}


@app.post("/db_user", response_model=UserInDB, summary="Insert a user into the database")
async def write_user(user: UserInDB):
    """
    Receives a fully-formed UserInDB instance and inserts it into the database
    without additional validation.
    """
    validator = UserValidator.get_instance()
    try:
        # Directly insert the user instance into the DB via manager
        validator.insert_user(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/db_user", response_model=UserInDB, summary="Get a user by user_id or email")
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
