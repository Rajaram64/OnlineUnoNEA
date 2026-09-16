import websockets
import asyncio
import json

clients = []
Lobbies = []
async def handle_hosts(connection):
    global clients
    global Lobbies
    try:
        package = await connection.recv()
        packet = json.loads(package)
        username = str(packet["hostpackage"][0]["username"])
        room_code = int(packet["hostpackage"][0]["room code"])
        host = [username, room_code]
        clients.append(username)
        confirmation = f"username recieved by server and sent by client {username}"
        await connection.send(confirmation)
        print(f"client {username} connected")
        print(f"clients: {clients}")
        Lobbies.append(host)
        print(f"hosts: {Lobbies}")
    except Exception as e:
        print(f"error: {type(e).__name__} {e}")

async def main():
    server = await websockets.serve(handle_hosts, "localhost", 8765)
    await asyncio.Future()
asyncio.run(main())
