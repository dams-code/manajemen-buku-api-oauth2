from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    nama: str
    role: str
    
class User(UserBase):
    password: str
    
class ResultUser(BaseModel):
    status: str
    pesan: str
    username: str
    role: str
    