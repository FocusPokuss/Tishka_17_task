import socket
import threading


HEAD_LEN = 4

active_sockets = []


def handle_connections(clients):
    while True:
        for client in clients:
            try:
                msg = my_recv(client)
                if msg is None:
                    continue
                client.sendall(f'{len(msg):0{HEAD_LEN}}'.encode('utf-8') + msg)
            except BlockingIOError:
                continue


def my_recv(sock):
    head = sock.recv(HEAD_LEN)
    if head == b'':
        active_sockets.remove(sock)
        sock.close()
        print('DISCONNECTED')
        return
    while len(head) < HEAD_LEN:
        head += sock.recv(HEAD_LEN-len(head))

    head = int(head)
    data = sock.recv(head)
    while len(data) < head:
        data += sock.recv(head-len(data))

    return data


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)
    server_socket.bind(('localhost', 8877))
    server_socket.listen()

    print('server is running...')
    thread = threading.Thread(target=handle_connections, args=(active_sockets,))
    thread.start()
    while True:
        try:
            conn, addr = server_socket.accept()
            active_sockets.append(conn)

        except (BlockingIOError, TimeoutError):
            pass  # xd

        except KeyboardInterrupt:
            for s in active_sockets:
                s.close()


if __name__ == '__main__':
    main()
