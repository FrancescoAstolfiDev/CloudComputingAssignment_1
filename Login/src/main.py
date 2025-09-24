import httpx
import requests
from fastapi import FastAPI, HTTPException

from .config import settings
from .schemas import UserResponse, UserCreate, LoginRequest
from .validator import UserValidator

app = FastAPI(title=settings.app_name)
# Root endpoint
@app.get("/")
async def root():
    return {"message": " Login Service"}


@app.post("/login", response_model=UserResponse, summary="Authenticate a user")
async def login(request: LoginRequest):
    validator = UserValidator.get_instance()
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(settings.db_address, params={"identifier": request.identifier})
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="User not found")
        user_data = resp.json()
        res = validator.matching_pswd(request.password, user_data.get("hashed_password"))
        if res is False:
            raise HTTPException(status_code=401, detail="Invalid user ID or password")
        print("out ottenuto dalla richiesta del db")
        print(user_data)
        return validator.out_user(user_data)

    except httpx.RequestError as exc:
        print(f"❌ Communication error to the DB service: {type(exc).__name__} - {str(exc)}")
        raise HTTPException(status_code=500, detail="DB Service not reachable")




# Create a new user
@app.post("/create", response_model=UserResponse, summary="Create a new user")
async def create_user(user: UserCreate):
    validator = UserValidator.get_instance()
    try:
        # Generate a new user
        user_obj = validator.create_user(user)

        # Write call
        async with httpx.AsyncClient() as client:
            resp = await client.post(settings.db_address, json=user_obj.dict())

        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Error creating user in DB")

        created_user = resp.json()
        # Write a response for the client
        out = validator.out_user(created_user)
        return out

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="DB Service not reachable")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/login/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}


