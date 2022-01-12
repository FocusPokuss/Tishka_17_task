import socket
from random import randint


HEAD_LEN = 4


def create_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8877))
    return s


def my_send(client_socket, data):
    encoded = data.encode('utf-8')
    head = f'{len(encoded):0{HEAD_LEN}}'.encode('utf-8')
    client_socket.sendall(head + encoded)


def my_recv(sock):
    head = sock.recv(HEAD_LEN)
    while len(head) < HEAD_LEN:
        head += sock.recv(HEAD_LEN - len(head))
    full_msg = b''
    while len(full_msg) < int(head):
        full_msg += sock.recv(int(head) - len(full_msg))
    return full_msg.decode('utf-8')


def main():
    clients = [create_client() for i in range(10)]
    try:
        while True:
            n = randint(0, 9)
            client = clients[n]
            msg = input()
            try:
                my_send(client, f'{msg} [FROM {n}]')
                print(my_recv(client))
            except ConnectionResetError:
                print('server is offline')

    except KeyboardInterrupt:
        for sock in clients:
            sock.close()


if __name__ == '__main__':
    main()

