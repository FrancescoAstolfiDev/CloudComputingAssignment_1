from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import httpx
from starlette.middleware.cors import CORSMiddleware

from .config import settings
from .schemas import LoginRequest, UserCreate, UserBasicInfo

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oppure ["http://localhost:3000"] per React dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API Gateway Login Service"}


@app.post("/login/user")
async def login(request: LoginRequest):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                settings.login_address + "/login",
                json=request.model_dump()
            )

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Login failed")

        user_data = resp.json()
        user_id = user_data.get("user_id") or user_data.get("identifier")

        return {"user_id": user_id}

    except httpx.RequestError as exc:
        print(f"❌ Communication error with login service: {type(exc).__name__} - {exc}")
        raise HTTPException(status_code=500, detail="Login service not reachable")


@app.post("/create/user")
async def create_user(user: UserCreate):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                settings.login_address + "/create",
                json=user.model_dump()
            )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            media_type=resp.headers.get("content-type")
        )
    except httpx.RequestError as exc:
        print(f"❌ Communication error with login service: {type(exc).__name__} - {exc}")
        raise HTTPException(status_code=500, detail="Login service not reachable")


@app.get("/user", response_model=UserBasicInfo)
async def show_homepage(identifier: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                settings.homepage_address + "/user",
                params={"identifier": identifier}
            )

        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="User not found in homepage service")

        user_data = resp.json()
        return UserBasicInfo(**user_data)

    except httpx.RequestError as exc:
        print(f"❌ Communication error with homepage service: {type(exc).__name__} - {exc}")
        raise HTTPException(status_code=500, detail="Homepage service not reachable")
    except ValueError as e:
        print(f"❌ Internal error parsing homepage response: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid response from homepage service")


@app.put("/user")
async def edit_params(user: UserBasicInfo):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.put(
                settings.homepage_address + "/user",
                json=user.model_dump()
            )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            media_type=resp.headers.get("content-type")
        )
    except httpx.RequestError as exc:
        print(f"❌ Communication error with homepage service: {type(exc).__name__} - {exc}")
        raise HTTPException(status_code=500, detail="Homepage service not reachable")

@app.get("/APIgateway/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}
