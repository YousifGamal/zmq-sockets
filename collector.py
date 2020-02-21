from commonfunctions import *


context = zmq.Context()

#  Socket to get binary images
socket_pull = context.socket(zmq.PULL)

socket_pull.bind("tcp://127.0.0.1:5656")

#socket to send the boxes (contours)

socket_push = context.socket(zmq.PUSH)

socket_push.bind("tcp://127.0.0.1:5569")

while True:
    msg = socket_pull.recv_json()
    socket_push.send_json(msg)