import socket
import threading


HEAD_LEN = 4


def handle_connection(sock, addr):
    print(f'new connection from: {addr}')
    while True:
        head = sock.recv(HEAD_LEN)

        if head == b'':
            print('DISCONNECT')
            break

        while len(head) < HEAD_LEN:
            head += sock.recv(HEAD_LEN-len(head))

        head = int(head)
        data = sock.recv(head)
        while len(data) < head:
            data += sock.recv(head-len(data))

        sock.sendall(head + data)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8877))
    server_socket.listen()

    print('starting server...')
    while True:
        client_sock, client_addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(client_sock, client_addr))
        thread.start()


if __name__ == '__main__':
    main()
