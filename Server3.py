import websockets
import asyncio
import json

lobbies = {} #key is roomcode, wkith data being a set of users. first user in set is host (forst to join therefore they created it)
async def handle_client_connections(connection):
    global lobbies

    packet = await connection.recv()
    packet = json.loads(packet)
    username = str(packet["package"][0]["username"])
    print(username)
    roomcode = int(packet["package"][0]["room code"])
    print(roomcode)
    type = str(packet["package"][0]["type"])
    print(type)

    if type == "HC":
        lobbies[roomcode] = set([username])
        confirmation = f"host {username} connected and created lobby {roomcode}"
        await connection.send(confirmation)

    elif type == "JL":
        lobbies[roomcode].add(username)
        confirmation = f"{username} joined lobby {roomcode}"
        await connection.send(confirmation)
        print(lobbies)
    else:
        confirmation = f"sent invalid type or invalid username or idk bro"
        await connection.send(confirmation)

async def main():
    server = await websockets.serve(handle_client_connections, "localhost", 8765)
    await asyncio.Future()

asyncio.run(main())
