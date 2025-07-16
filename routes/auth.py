from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from models.models import User
from database import engine
from auth import hash_password, verify_password, create_access_token, get_user_by_username

auth_router = APIRouter()

# Modelos de entrada para los requests
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    
@auth_router.post("/register")
def register(form_data: RegisterRequest):
    with Session(engine) as session:
        user_exist = get_user_by_username(form_data.username)
        if user_exist:
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        user = User(
            username=form_data.username,
            email=form_data.username,  
            hashed_password=hash_password(form_data.password)
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": "Usuario creado"}

@auth_router.post("/login")
def login(form_data: LoginRequest):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

