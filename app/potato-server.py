import asyncio
import mysql.connector
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()

try:
    db_config = mysql.connector.connect(
        host = 'plant-db', #nombre del docker donde corre la db
        database = os.getenv('MYSQL_DATABASE'),
        user = os.getenv('MYSQL_USER'),
        password = os.getenv('MYSQL_PASSWORD'),
        port = 3306
    )
    print("Conexion a la db exitosa")

except mysql.connector.Error as err:
    print(f"Error al conectar con la db: {err}")
    exit(1)

def is_valid_mac(mac):
    return re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac)

def is_valid_humidity(hum):
    try:
        value = float(hum)
        return 0 <= value <= 100
    except ValueError:
        return False

def insert_data(mac,hum):
    current_time = datetime.now()

    try:
        cursor = db_config.cursor()
        query = "INSERT INTO plantSense (mac, humedity, fecha) VALUES (%s, %s, %s)"
        cursor.execute(query, (mac, hum, current_time))
        db_config.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al insertar datos: {err}")
        return False

async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    print(f"Conexión desde: {address}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:  # El cliente cerró la conexión
                break

            message = data.decode().strip()
            print(f"Datos recibidos de {address}: {message}")

            try:
                mac, hum = message.split(",")
                if is_valid_mac(mac) and is_valid_humidity(hum):
                    if insert_data(mac, float(hum)):
                        writer.write(b"datos almacenados\n")
                    else:
                        writer.write(b"Error al almacenar datos\n")
                else:
                    writer.write(b"Formato invalido\n")
            except ValueError:
                writer.write(b"Datos mal formateados\n")


            await writer.drain()

    except Exception as e:
        print(f"Error con {address}: {e}")
        import traceback
        traceback.print_exc()  # Mostrar el seguimiento del error
        writer.write(b"Error interno del servidor\n")
        await writer.drain()
    finally:
        print(f"Conexión cerrada: {address}")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 9011)
    address = server.sockets[0].getsockname()
    print(f"Servidor escuchando en {address}")

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nServidor detenido")
    if db_config.is_connected():
        db_config.close()
