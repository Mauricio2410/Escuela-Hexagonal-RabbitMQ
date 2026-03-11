from pydantic import BaseModel

class Alumno(BaseModel):
    matricula: str
    nombre: str
    carrera: str