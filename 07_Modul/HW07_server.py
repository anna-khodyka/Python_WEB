import socket


def chat_server(host, port):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            with conn:
                data = conn.recv(1024)
                print(f'Server recived from client: {data.decode()}')
                if data == b"exit":
                    conn.sendall(b'exit')
                    print('Server sent "exit" to the client')
                    return False
                else:
                    conn.sendall(b'OK')
                    print('Server sent "OK" to the client')


def main():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 55555
    chat_server(SERVER_HOST, SERVER_PORT)


if __name__ == "__main__":
    main()
