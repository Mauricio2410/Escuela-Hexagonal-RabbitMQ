from abc import ABC, abstractmethod
from dominio.modelos import Alumno

class RepositorioAlumno(ABC):
    @abstractmethod
    def guardar_alumno(self, alumno: Alumno): pass
    @abstractmethod
    def obtener_todos(self): pass

class PublicadorEventos(ABC):
    @abstractmethod
    async def notificar_inscripcion(self, alumno: Alumno): pass