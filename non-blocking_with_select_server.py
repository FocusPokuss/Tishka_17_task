import socket
import select


HEAD_LEN = 4

active_sockets = []


def proceed_readable(rdy_to_read, server_socket):
    for sock in rdy_to_read:
        if sock is server_socket:
            print('NEW CONNECTION!')
            conn, addr = sock.accept()
            active_sockets.append(conn)
        else:
            head = sock.recv(HEAD_LEN)

            if head == b'':
                sock.close()
                active_sockets.remove(sock)
                print('DISCONNECTED')
                continue

            while len(head) < HEAD_LEN:
                head += sock.recv(HEAD_LEN-len(head))

            head = int(head)
            data = sock.recv(head)
            while len(data) < head:
                data += sock.recv(head-len(data))

            sock.sendall(f'{len(data):0{HEAD_LEN}}'.encode('utf-8') + data)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)
    server_socket.bind(('localhost', 8877))
    server_socket.listen()

    active_sockets.append(server_socket)

    print('server is starting...')
    while True:
        rdy_to_read, rdy_to_write, _ = select.select(active_sockets, [], [])
        proceed_readable(rdy_to_read, server_socket)


if __name__ == '__main__':
    main()
