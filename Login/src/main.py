import httpx
import requests
from fastapi import FastAPI, HTTPException

from .config import settings
from .schemas import UserResponse, UserCreate, LoginRequest
from .validator import UserValidator

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
        async with httpx.AsyncClient() as client:
            resp = await client.get(DB_SERVICE_URL, params={"identifier": request.identifier})
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


    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="DB Service not reachable")



# Create a new user
@app.post("/create", response_model=UserResponse, summary="Create a new user")
async def create_user(user: UserCreate):
    validator = UserValidator.get_instance()
    try:
        # Genera il nuovo utente tramite validator
        user_obj = validator.create_user(user)

        # Chiamata asincrona al DB service
        async with httpx.AsyncClient() as client:
            resp = await client.post(DB_SERVICE_URL, json=user_obj.dict())

        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Error creating user in DB")

        created_user = resp.json()
        print("out ottenuto dalla scritta del db")
        print(created_user)

        # Prepara la risposta per il client
        out = validator.out_user(created_user)
        return out

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="DB Service not reachable")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


