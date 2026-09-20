from repositories.user import result_update_user
from schemas.user import UserUpdate
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Query, Path
from repositories.user import *
from schemas.user import ResultUser, UserBase

from helpers.security import *

from typing import Annotated

router_user = APIRouter(tags=["user"])

@router_user.post("/login", response_model=ResultUser[UserBase])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    return await result_login(form_data=form_data)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router_user.get("/users", response_model=ResultUser[UserBase |list[UserBase]])
async def get_user(id: Annotated[int, Query()] = None, username: Annotated[str, Query()]=None, token: Annotated[OAuth2PasswordBearer, Depends(oauth2_scheme)] = None):
    return await result_get_user(id=id, username=username, token=token)

@router_user.post("/logout")
async def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    
    return await result_logout(token=token)

@router_user.post("/registrasi")
async def registrasi(registrasi_user: User):

    return await result_registrasi(registrasi_user)

@router_user.get("/user/aktif", response_model=ResultUser[UserBase])
async def get_user_id(token: Annotated[str, Depends(oauth2_scheme)]):

    return await result_get_user_id(token=token)

@router_user.put("/user/update/{username}")
async def update_user(username: str, update_user: UserUpdate, token: Annotated[str, Depends(oauth2_scheme)] = None):
    return await result_update_user(username, update_user, token)

router_user.put("/user/update/password")
async def update_password(username: str, update_password: str, token: Annotated[str, Depends(oauth2_scheme)]):
    return await result_update_password_user(username, update_password=update_password, token=token)
