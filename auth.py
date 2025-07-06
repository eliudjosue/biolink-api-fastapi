from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from database import engine
from models.models import User
from typing import Optional
from datetime import datetime, timedelta

# 🔐 Clave secreta y algoritmo
SECRET_KEY = "mi_super_secreta_clave"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hasheo de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tipo de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 👉 Hashear contraseña al registrarse
def hash_password(password: str):
    return pwd_context.hash(password)

# 👉 Verificar contraseña en login
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 👉 Crear token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 👉 Buscar usuario
def get_user_by_username(username: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.username == username)).first()

# 👉 Validar token y obtener usuario actual
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
