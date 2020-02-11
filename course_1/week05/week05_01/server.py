import socket
from time import sleep

# https://docs.python.org/3/library/socket.html
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8888))   # max port 65535
sock.listen(socket.SOMAXCONN)

conn, addr = sock.accept()
print('Connected by: {}'.format(addr))
message = None

mocked_data = "ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n"
try:
    while True:
        while (message is None) or (message.startswith('set')):
            data = conn.recv(1024)
            if not data:
                break
            # process data
            message = data.decode('utf-8')
        sleep(1)
        print('Out of cycle!')
        print(message, type(message), (message is not None), (message.startswith('get')))
        if (message is not None) and (message.startswith('get')):
            conn.sendall(mocked_data.encode("utf8"))
            print('Data sent!')
except KeyboardInterrupt:
    pass
conn.close()
sock.close()
