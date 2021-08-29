import socket
from time import sleep

RETRYING_ATTEMPTS = 3


def client_socket(host, port, message):
    with socket.socket() as s:
        try:
            s.connect((host, port))
            while True:
                s.sendall(bytes(message, encoding='utf-8'))
                data = s.recv(1024)  # а если он ничего не получит?
                print(f'Client recieved From server: {data.decode()}')
                if data == b'OK':
                    return True
                elif data == b'exit':
                    print('The client recieved the exit command and is closing...')
                    return False
                else:
                    print('Something went wrong...')
                    return False
        except ConnectionRefusedError:
            sleep(0.5)


def main():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 55555
    while True:
        message = input('Please, input message for server: ')
        if not client_socket(SERVER_HOST, SERVER_PORT, message):
            break


if __name__ == "__main__":
    main()
