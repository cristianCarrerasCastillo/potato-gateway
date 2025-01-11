import asyncio

async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    print(f"Conexión desde: {address}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:  # El cliente cerró la conexión
                break
            print(f"Datos recibidos de {address}: {data.decode()}")
            writer.write(b"Datos recibidos")
            await writer.drain()
    except Exception as e:
        print(f"Error con {address}: {e}")
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

asyncio.run(main())
