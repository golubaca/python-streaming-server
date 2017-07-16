import sys
import socket
import _thread
import time
import signal
from Libs import Connection





server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", 5005))
server_socket.listen(5)

connections = []
oppened_cameras = {}


def signal_handler(signal=None, frame=None):
    exit(0)

while 1:
    try:
        client_socket, address = server_socket.accept()
        print
        "Conencted to - ", address, "\n"
        cam_url = client_socket.recv(1024)
        if cam_url not in oppened_cameras:
            # oppened_cameras.append(cam_url)
            client = Connection.Connection([client_socket, cam_url])
            oppened_cameras[cam_url] = client
            _thread.start_new_thread(client.capture, (oppened_cameras,))

        else:
            oppened_cameras[cam_url].addConnection(client_socket)
        connections.append([client_socket, cam_url])

    except socket.timeout:
        continue
    except KeyboardInterrupt:
        # cap.release()
        server_socket.close()

        del connections
        exit(0)
