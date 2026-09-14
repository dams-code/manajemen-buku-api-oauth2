from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, Query
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
