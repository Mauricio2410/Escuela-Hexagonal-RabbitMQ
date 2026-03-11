from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dominio.modelos import Alumno
from aplicacion.puertos import RepositorioAlumno

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/escuela"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AlumnoModel(Base):
    __tablename__ = "alumnos"
    matricula = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(100))
    carrera = Column(String(100))

Base.metadata.create_all(bind=engine)

class AdaptadorMySQL(RepositorioAlumno):
    def __init__(self, db: Session):
        self.db = db

    def guardar_alumno(self, alumno: Alumno):
        db_alumno = AlumnoModel(matricula=alumno.matricula, nombre=alumno.nombre, carrera=alumno.carrera)
        self.db.add(db_alumno)
        self.db.commit()

    def obtener_todos(self):
        return self.db.query(AlumnoModel).all()