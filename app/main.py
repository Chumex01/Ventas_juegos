from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models 
from app.config import settings

# <-- IMPORTAMOS EL ROUTER DE ROLES -->
from app.routers import roles
from app.routers import usuarios # <-- IMPORTA EL ROUTER DE USUARIOS (AUTH)
from app.routers import auth # <-- IMPORTA EL ROUTER DE AUTENTICACIÓN

# --- CREACIÓN DE TABLAS AL INICIAR ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Creando tablas en la base de datos si no existen...")
    Base.metadata.create_all(bind=engine)
    print("✅ ¡Tablas comprobadas/creadas!")
    yield

# --- INICIALIZACIÓN DE LA APP ---
app = FastAPI(title="SERO v2.0 - Core Events & Audit", lifespan=lifespan)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# <-- CONECTAMOS EL ROUTER AQUÍ -->
app.include_router(roles.router)
app.include_router(usuarios.router) # <-- Asegúrate de importar el router de auth al inicio del archivo
app.include_router(auth.router) # <-- CONECTA EL ROUTER DE AUTENTICACIÓN