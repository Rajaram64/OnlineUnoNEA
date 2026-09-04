import websockets
import asyncio

clients = []
async def handle_usernames(connection):
    global clients
    try:
        usrname = await connection.recv()
        clients.append((connection, usrname))
        confirmation = f"username sent by server and recieved by client {usrname}"
        await connection.send(confirmation)
        print(f"client {usrname} connected")
        print(f"clients: {clients}")
    except:
        pass

async def main():
    server = await websockets.serve(handle_usernames, "localhost", 8765)
    await asyncio.Future()
asyncio.run(main())
