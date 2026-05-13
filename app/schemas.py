from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RolGet(BaseModel):
    id: int
    nombre_rol: str
    fecha_creacion: datetime
    estado: bool
    model_config = ConfigDict(from_attributes=True)
    
class RolCreate(BaseModel):
    nombre_rol: str
    
class UsuarioCreate(BaseModel):
    rol_id: int
    nombre: str
    primer_apellido: str
    segundo_apellido: str | None = None
    email: str
    hashed_password: str
    
class UsuarioGet(BaseModel):
    id: int
    rol_id: int
    nombre: str
    primer_apellido: str
    segundo_apellido: str | None = None
    email: str
    fecha_creacion: datetime
    estado: bool
    model_config = ConfigDict(from_attributes=True)
