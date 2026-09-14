from pydantic import BaseModel
from typing import Generic, Optional, TypeVar
from models.token import TokenSession

T = TypeVar('T')

class UserBase(BaseModel):
    username: str
    nama: str
    role: str
    
class User(UserBase):
    password: str
    
class UserInDB(UserBase):
    hash_password: str

class ResultUser(BaseModel, Generic[T]):
    status: int
    pesan: str
    data_user: Optional[T] = None
    data_token: Optional[TokenSession] = None

