import pika
import json
import sys

def callback(ch, method, properties, body):
    try:
        datos = json.loads(body.decode())
        matricula = datos['matricula']
        nombre = datos['nombre']
        carrera = datos['carrera']
        
        nombre_archivo = f"constancia_{matricula}.txt"
        
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("=========================================\n")
            f.write("         CONSTANCIA DE ESTUDIOS          \n")
            f.write("=========================================\n\n")
            f.write(f"El alumno(a): {nombre}\n")
            f.write(f"Con matricula: {matricula}\n")
            f.write(f"Se encuentra inscrito(a) en la carrera de: {carrera}.\n\n")
            f.write("=========================================\n")
            f.write("Universidad Autonoma de Chiapas (UNACH)\n")
        
        print(f" [x] Tarea Secundaria Completada: {nombre_archivo} generado.")
        
    except Exception as e:
        print(f" [!] Error al procesar el mensaje: {e}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='unachlidts')
    channel.basic_consume(queue='unachlidts', on_message_callback=callback, auto_ack=True)
    
    print(' [*] Tarea Secundaria (Constancias) activa. Esperando alumnos...')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido')
        sys.exit(0)