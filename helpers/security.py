from itsdangerous import TimestampSigner, SignatureExpired, BadTimeSignature
from fastapi import HTTPException, status
from dotenv import load_dotenv

import os

load_dotenv()

GET_SECRET_KEY = os.getenv("SECRET_KEY")

if GET_SECRET_KEY is None:
    raise RuntimeError("File .env belum dibuat / tidak ditemukan")

signer = TimestampSigner(GET_SECRET_KEY)


def create_access_token(username: str):
    token = signer.sign(username).decode("UTF-8")
    return token

def verify_access_token(token: str, umur_token: int = 3600) -> str:
    try:
        username = signer.unsign(token, max_age=umur_token).decode("UTF-8")
        return username
    except SignatureExpired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sudah expired / kadaluwarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except BadTimeSignature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid",
            headers={"WWW-Authenticate": "Bearer"},
        )