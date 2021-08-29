import asyncio
import socket


async def handle_client(client):
    loop = asyncio.get_event_loop()
    request = None
    while request != 'exit':
        request = (await loop.sock_recv(client, 255)).decode('utf8')
        print(request)
        response = 'OK'
        await loop.sock_sendall(client, response.encode('utf8'))
    client.close()


async def run_server(s_host, s_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((s_host, s_port))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, addr = await loop.sock_accept(server)
        print(f"Connected by {addr}")
        loop.create_task(handle_client(client))


if __name__ == "__main__":

    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 55555
    asyncio.run(run_server(SERVER_HOST, SERVER_PORT))
