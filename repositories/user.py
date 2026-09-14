from helpers.security import create_access_token
from schemas.user import UserInDB
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import *
from models.token import *
from helpers.helper_password_user import verify_password, get_password_hash
from helpers.security import *

# import secrets

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

    # secret_token = secrets.token_hex(32)
    # temp_token[secret_token] = user_aktif.username

    access_token = create_access_token(username=form_data.username)

    return ResultUser[UserBase](
        status=status.HTTP_200_OK,
        pesan=f"User {form_data.username} berhasil login",
        data_user=UserBase(**user_aktif.model_dump()),
        data_token=TokenSession(
            # access_token=list(temp_token.keys())[0],
            access_token = access_token,
            token_type="bearer",
            username=form_data.username
        )
    )

async def result_get_user(id: int | None, username: str | None, token: str | None) -> ResultUser[UserBase | list[UserBase]]:

    if not token:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak ada / wajib disertakan",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # cek_username_aktif = next((user for user in data_user if user["username"].lower() == temp_token.get(token, "").lower()), None)

    cek_username_aktif  = verify_access_token(token, 3600)

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

async def result_logout(token: str) -> ResultUser[None]:
    if token in temp_token:
        del temp_token[token]

    cek_username_aktif  = verify_access_token(token, 3600)

    return ResultUser[None](
        status=status.HTTP_200_OK,
        pesan=f"Anda sudah logout",
        data_user=None
    )


