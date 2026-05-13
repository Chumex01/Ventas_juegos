from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import get_current_active_user # <-- Importamos el candado
from app.audit import create_audit_log            # <-- Importamos la auditoría

router = APIRouter(prefix="/roles", tags=["Roles"])

# --- RUTA PARA OBTENER TODOS LOS ROLES (GET) ---
@router.get("/", response_model=list[schemas.RolGet])
def obtener_roles(db: Session = Depends(get_db), current_user: dict = Depends(get_current_active_user)):
    # Ahora esta ruta está protegida. Si no mandas el token, da error 401
    roles = db.query(models.Roles).all()
    return roles

# --- RUTA PARA CREAR UN ROL (POST) ---
@router.post("/", response_model=schemas.RolGet)
def crear_rol(
    rol: schemas.RolCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_active_user) # Exigimos usuario
):
    rol_existente = db.query(models.Roles).filter(models.Roles.nombre_rol == rol.nombre_rol).first()
    if rol_existente:
        raise HTTPException(status_code=400, detail="Este rol ya existe.")
    
    nuevo_rol = models.Roles(nombre_rol=rol.nombre_rol)
    db.add(nuevo_rol)
    
    # --- AUDITORÍA ---
    create_audit_log(
        db=db,
        user_id=current_user.id, # Sacamos el ID del usuario que firmó con el token
        tabla="roles",
        accion="CREAR",
        new_val={"nombre_rol": rol.nombre_rol, "estado": True}
    )
    # ------------------------------------------------
    
    # HACEMOS UN SOLO COMMIT AL FINAL (Si algo falla antes, no guarda ni el rol ni la auditoría)
    db.commit() 
    db.refresh(nuevo_rol)
    
    return nuevo_rol