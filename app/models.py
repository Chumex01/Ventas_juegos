from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(30), unique=True, index=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)

class Usuarios(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey('roles.id'))
    nombre = Column(String(50), unique=True, index=True)
    primer_apellido = Column(String(50))
    segundo_apellido = Column(String(50), nullable=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    rol = relationship("Roles", backref="usuarios")

class Clientes(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True)
    primer_apellido = Column(String(50))
    segundo_apellido = Column(String(50), nullable=True)
    email = Column(String(100), unique=True, index=True)
    telefono = Column(String(100), nullable=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)

class Direcciones(Base):
    __tablename__ = "direcciones"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    direccion = Column(String(255))
    ciudad = Column(String(100))
    pais = Column(String(100))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    cliente = relationship("Clientes", backref="direcciones") # Cambiado de cliente_id_rel

class Videojuegos(Base):
    __tablename__ = "videojuegos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True)
    descripcion = Column(Text)
    fecha_lanzamiento = Column(DateTime)
    precio = Column(Float(10, 2))
    tipo = Column(String(50))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)

class Inventario_fisico(Base):
    __tablename__ = "inventario_fisico"
    id = Column(Integer, primary_key=True, index=True)
    videojuego_id = Column(Integer, ForeignKey('videojuegos.id'))
    cantidad_stock = Column(Integer)
    ubicacion = Column(String(100))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    videojuego = relationship("Videojuegos", backref="inventario_fisico") # Cambiado

class Inventario_digital(Base):
    __tablename__ = "inventario_digital"
    id = Column(Integer, primary_key=True, index=True)
    videojuego_id = Column(Integer, ForeignKey('videojuegos.id'))
    tamaño_archivo = Column(String(10))
    requisitos_sistema = Column(Text)
    codigo_licencia = Column(String(100), unique=True, index=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    videojuego = relationship("Videojuegos", backref="inventario_digital") # Cambiado

class Categorias(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)

class Videojuego_categoria(Base):
    __tablename__ = "videojuego_categoria"
    id = Column(Integer, primary_key=True, index=True)
    videojuego_id = Column(Integer, ForeignKey('videojuegos.id'))
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    videojuego = relationship("Videojuegos", backref="categorias_rel") # Cambiado
    categoria = relationship("Categorias", backref="videojuegos_rel")   # Cambiado

class Plataformas(Base):
    __tablename__ = "plataformas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)

class Videojuego_plataforma(Base):
    __tablename__ = "videojuego_plataforma"
    id = Column(Integer, primary_key=True, index=True)
    videojuego_id = Column(Integer, ForeignKey('videojuegos.id'))
    plataforma_id = Column(Integer, ForeignKey('plataformas.id'))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    videojuego = relationship("Videojuegos", backref="plataformas_rel") # Cambiado
    plataforma = relationship("Plataformas", backref="videojuegos_rel") # Cambiado

class Tipo_pago(Base): # Cambiado a mayúscula (convención PEP8)
    __tablename__ = "tipo_pago"
    id = Column(Integer, primary_key=True, index=True)
    nombre_tipo_pago = Column(String(50), unique=True, index=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)

class Pagos(Base):
    __tablename__ = "pagos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    tipo_pago_id = Column(Integer, ForeignKey('tipo_pago.id'))
    monto = Column(Float(10, 2))
    fecha_pago = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    cliente = relationship("Clientes", backref="pagos")       # Cambiado
    tipo_pago = relationship("Tipo_pago", backref="pagos")    # Cambiado

class Detalle_pago(Base):
    __tablename__ = "detalle_pago"
    id = Column(Integer, primary_key=True, index=True)
    pago_id = Column(Integer, ForeignKey('pagos.id'))
    videojuego_id = Column(Integer, ForeignKey('videojuegos.id'))
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(Float(10, 2))
    total = Column(Float(10, 2))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    pago = relationship("Pagos", backref="detalles")           # Cambiado
    videojuego = relationship("Videojuegos", backref="detalles") # Cambiado

class Descuentos(Base):
    __tablename__ = "descuentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre_descuento = Column(String(50), unique=True, index=True)
    porcentaje_descuento = Column(Float(5, 2))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)

class Videojuego_descuento(Base):
    __tablename__ = "videojuego_descuento"
    id = Column(Integer, primary_key=True, index=True)
    videojuego_id = Column(Integer, ForeignKey('videojuegos.id'))
    descuento_id = Column(Integer, ForeignKey('descuentos.id'))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    videojuego = relationship("Videojuegos", backref="descuentos") # Cambiado
    descuento = relationship("Descuentos", backref="videojuegos")   # Cambiado

class Pedidos(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    pago_id = Column(Integer, ForeignKey('pagos.id'))
    direccion_id = Column(Integer, ForeignKey('direcciones.id'))
    fecha_pedido = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_envio = Column(DateTime, nullable=True)
    fecha_entrega = Column(DateTime, nullable=True)
    estado_pedido = Column(String(20))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    pago = relationship("Pagos", backref="pedidos")             # Cambiado
    direccion = relationship("Direcciones", backref="pedidos")   # Cambiado

class Biblioteca_cliente(Base):
    __tablename__ = "biblioteca_cliente"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    videojuego_id = Column(Integer, ForeignKey('videojuegos.id'))
    fecha_adquisicion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado = Column(Boolean, default=True)
    
    cliente = relationship("Clientes", backref="biblioteca")       # Cambiado
    videojuego = relationship("Videojuegos", backref="biblioteca") # Cambiado

class Auditoria(Base):
    __tablename__ = "auditoria"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    accion = Column(String(255))
    tabla = Column(String(50))
    datos_antiguos = Column(JSON, nullable=True)
    datos_nuevos = Column(JSON, nullable=True)
    fecha_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    usuario = relationship("Usuarios", backref="auditorias") # Cambiado