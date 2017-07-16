#!/usr/bin/python
import socket
import cv2
import numpy
import random
import sys

host = sys.argv[1] # e.g. localhost, 192.168.1.123
cam_url = sys.argv[2] # rtsp://user:pass@url/live.sdp , http://url/video.mjpg ...
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect((host, 5005))
name = str(random.random()) # gives random name to create window

client_socket.send(str.encode(cam_url))

def rcv():
    data = b''
    while 1:
        
        try:
            r = client_socket.recv(90456)
            if len(r) == 0:
                exit(0)
            a = r.find(b'END!')
            if a != -1:
                data += r[:a]
                break
            data += r
        except Exception as e:
            print(e)
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
