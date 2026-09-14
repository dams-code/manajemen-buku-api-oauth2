from schemas.user import UserInDB
from fastapi import Query, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user import *
from models.token import *
from helpers.helper_password_user import verify_password, get_password_hash

import secrets

temp_token: dict[str, str] = {}

data_user = [
    {
        "id": 1,
        "username": "test1",
        "nama": "user test 1",
        "hash_password": get_password_hash("test1"),
        "role": "admin"
    }
]

async def result_login(form_data: OAuth2PasswordRequestForm) -> ResultUser[UserBase]:
    
    result_data_user = next((user for user in data_user if user["username"].lower() == form_data.username.lower()) ,None)

    if result_data_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Username {form_data.username} tidak ditemukan",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_aktif = UserInDB(**result_data_user)
    
    if not verify_password(form_data.password, user_aktif.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Password yang dimasukkan salah",
            headers={"WWW-Authenticate": "Bearer"}
        )

    secret_token = secrets.token_hex(32)

    temp_token[secret_token] = user_aktif.username

    return ResultUser[UserBase](
        status=status.HTTP_200_OK,
        pesan=f"User {form_data.username} berhasil login",
        data_user=UserBase(**user_aktif.model_dump()),
        data_token=TokenSession(
            access_token=list(temp_token.keys())[0],
            token_type="bearer",
            username=form_data.username
        )
    )

async def result_get_user(id: int | None, username: str | None, token: str | None) -> ResultUser[UserBase | list[UserBase]]:

    cek_username_aktif = next((user for user in data_user if user["username"].lower() == temp_token.get(token, "").lower()), None)

    if cek_username_aktif is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token tidak valid",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if id is not None or username is not None:
        result_data_user = next((user for user in data_user if (id is None or user["id"] == id) and (username is None or user["username"].lower() == username.lower()) ), None)

        if result_data_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User id {id} tidak ditemukan"
            )

        return ResultUser[UserBase](
            status= status.HTTP_200_OK,
            pesan= f"Data user id {result_data_user['id']} - username {result_data_user['username']} berhasil terload",
            data_user= UserBase(**result_data_user)
        )

    list_user = [UserBase(**user) for user in data_user]

    return ResultUser[list[UserBase]](
        status=status.HTTP_200_OK,
        pesan=f"User berhasil terload (total {len(list_user)} user)",
        data_user=list_user
    )




