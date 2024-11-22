from pydantic import BaseModel
from datetime import date, datetime

class UserBase(BaseModel):
    email: str
    nombre: str
    apellido: str
    fecha_nacimiento: date
    dni: str
    pais: str
    ciudad: str
    direccion: str
    telefono: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

