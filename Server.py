import websockets
import asyncio

async def recieve_username(connection):
    username = await connection.recv()
    print(f"recieved username: {username}")
    confirmation = f"username sent by server and recieved by client {username}"
    await connection.send(confirmation)
    print("server sent confirmation")
    return username

async def main():
    server = await websockets.serve(recieve_username, "localhost", 8765)
    await asyncio.Future() #will run continously
asyncio.run(main())
