from base64 import b64encode

from fastapi import FastAPI, HTTPException, APIRouter, Body
from sqlalchemy.orm import Session  # type: ignore
from sql_app import persistence, models, schemas, twitter_client
from sql_app.database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.post("/login")
async def login(username: str = Body(...), password: str = Body(...)):
    u = persistence.get_user_by_name(username)
    if not u:
        raise HTTPException(401, "User not found")
    if not u.is_active:
        raise HTTPException(401, "Inactive user")
    if u.password != password:
        raise HTTPException(401, "Incorrect password")
    token = b64encode(f"{username}:{password}".encode()).decode("ascii")
    return {"result": "success", "token": token}


###################### identity -  ###############################################GET
# @router.get("/", response_model=list[schemas.Identity])
# async def read_identities(skip: int = 0, limit: int = 10):
#     ide = persistence.get_identiy(skip=skip, limit=limit)
#     return ide


# @router.get("/{user_name}", response_model=schemas.Identity)
# async def read_identity(user_name: str):
#     db_identity = persistence.get_identiy_by_name(s_name=user_name)
#     if db_identity is None:
#         raise HTTPException(
#             status_code=404, detail="Identiy not found for user {user_name}"
#         )
#     return db_identity


# @router.get("/social/{social_network}")
# async def read_identity_social(social_network: int):
#     db_identity = persistence.get_identiy_by_network(s_network=social_network)
#     if db_identity is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Identiy not found for social network {social_network}",
#         )
#     return db_identity


# ####POST
# @router.post("/users/", response_model=schemas.Identity)
# async def create_identity_for_user(identity: schemas.IdentityCreate):
#     return persistence.create_identity_social_user(identity=identity)


# ###PUT
# @router.patch("/put/{user}/{network}/{id_on_network}")
# async def update_identity_user(user: str, network: int, id_on_network: int):
#     identity = schemas.IdentityUpdate(id_on_network=id_on_network)
#     return persistence.update_identity_social_user(
#         s_network=network, appuser=user, identity=identity
#     )


# ###DELETE
# @router.delete("/{user}/{network}/")
# async def delete_identity_user(user: str, network: int):
#     return persistence.delete_identity_social_user(s_network=network, appuser=user)


############################# FINE IDENTITY ##################################
