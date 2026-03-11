from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dominio.modelos import Alumno
from aplicacion.casos_uso import InscribirAlumnoUseCase, ListarAlumnosUseCase
from infraestructura.bd_mysql import SessionLocal, AdaptadorMySQL
from infraestructura.rabbit import AdaptadorRabbitMQ

app = FastAPI(title="API Escuela Hexagonal")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.post("/alumnos/")
async def inscribir_alumno(alumno: Alumno, db: Session = Depends(get_db)):
    repo = AdaptadorMySQL(db)
    pub = AdaptadorRabbitMQ()
    caso_uso = InscribirAlumnoUseCase(repo, pub)
    return await caso_uso.ejecutar(alumno)

@app.get("/alumnos/")
def listar_alumnos(db: Session = Depends(get_db)):
    repo = AdaptadorMySQL(db)
    caso_uso = ListarAlumnosUseCase(repo)
    return caso_uso.ejecutar()