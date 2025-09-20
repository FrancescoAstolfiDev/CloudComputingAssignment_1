import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from src.config import settings
from src.model import UserInDB
from src.schemas import UserResponse, UserCreate, LoginRequest
from src.validator import UserValidator

app = FastAPI(title=settings.app_name)
DB_SERVICE_URL = "http://localhost:8000/db_user"  # URL del tuo DB service
# Root endpoint
@app.get("/")
async def root():
    return {"message": " Login Service"}

# Schema per login


@app.post("/login", response_model=UserResponse, summary="Authenticate a user")
async def login(request: LoginRequest):
    validator = UserValidator.get_instance()
    try:
        # Chiamata GET al DB service
        resp = requests.get(DB_SERVICE_URL, params={"identifier": request.identifier})
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="User not found")
        user_data = resp.json()
        print("prima del matching")
        res=validator.matching_pswd(request.password, user_data.get("hashed_password"))
        if res is False:
            raise HTTPException(status_code=401, detail="Invalid user ID or password")
        print("out ottenuto dalla richiesta del db")
        print(user_data)
        return validator.out_user(user_data)

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="DB Service not reachable")


# Create a new user
@app.post("/create", response_model=UserResponse, summary="Create a new user")
async def create_user(user: UserCreate):
    validator = UserValidator.get_instance()
    try:
        user=validator.create_user(user)
        request = requests.post(DB_SERVICE_URL, json=user.dict())
        created_user = request.json()
        print("out ottenuto dalla scritta del db")
        print(created_user)
        out=validator.out_user(created_user)
        return out
    except ValueError as e:
        # Handle validation errors (e.g., email exists, password invalid)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")


