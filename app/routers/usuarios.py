from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.audit import create_audit_log
from app.database import get_db
from app.security import get_current_active_user, get_password_hash


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=schemas.UsuarioGet)
def crear_usuario(
    usuario: schemas.UsuarioCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_active_user) # Exigimos usuario
):
    usuario_existente = db.query(models.Usuarios).filter(models.Usuarios.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este email ya está registrado.")
    
    nuevo_usuario = models.Usuarios(
        rol_id=usuario.rol_id,
        nombre=usuario.nombre,
        primer_apellido=usuario.primer_apellido,
        segundo_apellido=usuario.segundo_apellido,
        email=usuario.email,
        hashed_password=get_password_hash(usuario.hashed_password)
    )
    db.add(nuevo_usuario)
    
    # --- AUDITORÍA ---
    create_audit_log(
        db=db,
        user_id=current_user["id"], # Sacamos el ID del usuario que firmó con el token
        tabla="usuarios",
        accion="CREAR",
        new_val={
            "rol_id": usuario.rol_id,
            "nombre": usuario.nombre,
            "primer_apellido": usuario.primer_apellido,
            "segundo_apellido": usuario.segundo_apellido,
            "email": usuario.email
        }
    )
    # ------------------------------------------------
    
    db.commit() 
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario