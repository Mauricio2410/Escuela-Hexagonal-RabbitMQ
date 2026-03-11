from dominio.modelos import Alumno
from aplicacion.puertos import RepositorioAlumno, PublicadorEventos

class InscribirAlumnoUseCase:
    def __init__(self, repositorio: RepositorioAlumno, publicador: PublicadorEventos):
        self.repositorio = repositorio
        self.publicador = publicador

    async def ejecutar(self, alumno: Alumno):
        self.repositorio.guardar_alumno(alumno)
        await self.publicador.notificar_inscripcion(alumno)
        return {"status": "Éxito", "mensaje": "Constancia TXT en proceso"}

class ListarAlumnosUseCase:
    def __init__(self, repositorio: RepositorioAlumno):
        self.repositorio = repositorio

    def ejecutar(self):
        return self.repositorio.obtener_todos()