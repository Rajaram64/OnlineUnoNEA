import websockets
import asyncio

clients = []
hosts = []
async def handle_hosts(connection):
    global clients
    global hosts
    try:
        package = await connection.recv()
        clients.append(package[0])
        confirmation = f"username sent by server and recieved by client {package[0]}"
        await connection.send(confirmation)
        print(f"client {package[0]} connected")
        print(f"clients: {clients}")
        hosts.append(package)
        print(f"hosts: {hosts}")
    except:
        print("error")

async def main():
    server = await websockets.serve(handle_hosts, "localhost", 8765)
    await asyncio.Future()
asyncio.run(main())
