from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import aio_pika

DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/usuarios/")
async def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

@app.post("/registrar/")
async def registrar_usuario(username: str, password: str, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(username=username, password=password)
    db.add(nuevo_usuario)
    db.commit()
    
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")
    async with connection:
        channel = await connection.channel()
        mensaje = f"REGISTRO: {username}"
        await channel.default_exchange.publish(
            aio_pika.Message(body=mensaje.encode()),
            routing_key="unachlidts"
        )
    return {"status": "Guardado", "usuario": username}

@app.put("/editar/{usuario_id}")
async def editar_usuario(usuario_id: int, nuevo_nombre: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No encontrado")

    usuario.username = nuevo_nombre
    db.commit()

    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")
    async with connection:
        channel = await connection.channel()
        mensaje = f"EDICIÓN: ID {usuario_id} ahora es {nuevo_nombre}"
        await channel.default_exchange.publish(
            aio_pika.Message(body=mensaje.encode()),
            routing_key="unachlidts"
        )
    return {"status": "Actualizado", "id": usuario_id}

@app.delete("/eliminar/{usuario_id}")
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No encontrado")

    db.delete(usuario)
    db.commit()

    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")
    async with connection:
        channel = await connection.channel()
        mensaje = f"ELIMINACIÓN: ID {usuario_id} borrado"
        await channel.default_exchange.publish(
            aio_pika.Message(body=mensaje.encode()),
            routing_key="unachlidts"
        )
    return {"status": "Eliminado", "id": usuario_id}