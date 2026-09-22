import websockets
import asyncio
import json

request_type = "HC"

clients = []
lobbies = [] #lobby will have sublists, each containing the roomcode as the first value, and then all usernames, and then tags for settings
usernames = []
async def handle_client_connections(connection):

    global clients
    global lobbies
    global usernames
    packet = await connection.recv()
    packet = json.loads(packet)
    username = str(packet["package"][0]["username"])
    print(username)
    roomcode = int(packet["package"][0]["room code"])
    print(roomcode)
    type = str(packet["package"][0]["type"])
    print(type)
    if type == "HC" and roomcode not in lobbies and username not in usernames and username != "":
        identifier = [username, roomcode, type]
        usernames.append(username)
        clients.append(identifier)
        lobbies.append([roomcode, [username, type]])
        confirmation = f"host {username} connected and created lobby {roomcode}"
        await connection.send(confirmation)
    elif type == "JL" and roomcode in lobbies and username not in usernames and username != "":
        identifier = [username, roomcode, type]
        usernames.append(username)
        clients.append(identifier)
        lobbies[roomcode].append([username, type])
        confirmation = f"{username} joined lobby {roomcode}"
        await connection.send(confirmation)
        print(lobbies)
        print(clients)
    else:
        confirmation = f"sent invalid type or invalid username or idk bro"
        await connection.send(confirmation)



async def main():
    global request_type
    if request_type == "HC":
        server = await websockets.serve(handle_client_connections, "localhost", 8765)
        await asyncio.Future()


asyncio.run(main())
