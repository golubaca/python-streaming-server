#!/usr/bin/python
# TCP client example
import socket,os, cv2
import numpy
import random
import sys

host = 'localhost' if len(sys.argv) == 1 else sys.argv[1]
cam_url = sys.argv[2]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect((host, 5005))
k = ' '
size = 1024
name = str(random.random())

client_socket.send(cam_url)

def rcv():
    r = ''
    data = ""
    while 1:
        try:
            r = client_socket.recv(90456)
            if len(r) == 0:
                exit(0)
            a = r.find('END!')
            if a != -1:
                data += r[:a]
                break
            data += r
        except Exception as e:
            print e
            continue
    nparr = numpy.fromstring(data, numpy.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if type(frame) is type(None):
        pass
    else:
        try:
            cv2.imshow(name,frame)
            if cv2.waitKey(10) == ord('q'):
                client_socket.close()
                sys.exit()
        except:
            client_socket.close()
            exit(0)

while 1:
    rcv()
