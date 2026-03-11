import aio_pika
import json
from dominio.modelos import Alumno
from aplicacion.puertos import PublicadorEventos

class AdaptadorRabbitMQ(PublicadorEventos):
    async def notificar_inscripcion(self, alumno: Alumno):
        connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")
        async with connection:
            channel = await connection.channel()
            datos = json.dumps({"matricula": alumno.matricula, "nombre": alumno.nombre, "carrera": alumno.carrera})
            await channel.default_exchange.publish(
                aio_pika.Message(body=datos.encode()),
                routing_key="unachlidts"
            )