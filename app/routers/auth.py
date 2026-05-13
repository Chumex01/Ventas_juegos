from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Importaciones de tu proyecto
from app.database import get_db
from app import schemas
from app.security import authenticate_user, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2PasswordRequestForm exige que mandes los datos como form-data (x-www-form-urlencoded)
    NO como JSON. Los campos se llaman 'username' y 'password' obligatoriamente.
    Como tu campo en la BD es 'nombre', lo mapeamos aquí.
    """
    
    # 1. Autenticar al usuario
    user = authenticate_user(db, nombre=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Crear el Token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre}, # "sub" es el estándar para guardar el identificador (en este caso el nombre)
        expires_delta=access_token_expires
    )
    
    # 3. Devolver el token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }