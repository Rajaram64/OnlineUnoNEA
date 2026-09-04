import websockets
import asyncio
async def send_username():
    connectionpoint = "ws://localhost:8765"
    connection = await websockets.connect(connectionpoint)
    username = input("enter username ")
    await connection.send(username)
    print("client sent username")
    confirmation = await connection.recv()
    print(confirmation)
asyncio.run(send_username())
