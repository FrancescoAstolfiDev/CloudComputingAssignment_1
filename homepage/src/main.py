from typing import Dict

import httpx
from fastapi import FastAPI, HTTPException

from .config import settings
from .schemas import User


app = FastAPI(title=settings.app_name)
# Root endpoint
@app.get("/")
async def root():
    return {"message": " Homepage Service"}


@app.get("/user", response_model=User, summary="It get the params for the user")
async def logged(identifier: str):
    """
        -the query is after the log of the user
        -i need a  user with uid and his params
        -the query should take an identifier and show the related params
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(settings.db_address, params={"identifier": identifier})
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="User not found")
        user_data = resp.json()
        return user_data

    except httpx.RequestError as exc:
        print(f"❌ Communication error to the DB service: {type(exc).__name__} - {str(exc)}")
        raise HTTPException(status_code=500, detail="DB Service not reachable")
    except ValueError as e:
        print(f"❌ Internal error wrong  out from the db  : {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=400, detail="DB Service not reachable")


# Create a new user
@app.put("/user", response_model=Dict[str,int], summary="Modify the params into the db ")
async def edit_user(user: User):
    """"
        -the query is after the log of the user
        -i need a  user with uid and his params
        -the query should take an identifier and show the related params
    """
    try:
        # write the data of the new params on the db
        print(user)

        # Chiamata asincrona al DB service
        async with httpx.AsyncClient() as client:
            resp = await client.put(settings.db_address, json=user.dict())

        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Error creating user in DB")

        # Prepara la risposta per il client
        return  resp.json()
        return out


    except httpx.RequestError as exc:
        print(f"❌ Communication error to the DB service: {type(exc).__name__} - {str(exc)}")
        raise HTTPException(status_code=500, detail="DB Service not reachable")
    except ValueError as e:
        print(f"❌ Internal error wrong  out from the db  : {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=400, detail="DB Service not reachable")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/homepage/health", summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}


