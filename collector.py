from commonfunctions import *
import sys
import time


collectorNumber = int(sys.argv[1])
collector1Port = str(5400 + collectorNumber)
collector1PortPush = str(5600 + collectorNumber)
print("created: collector1 number ",collectorNumber,collector1Port,collector1PortPush)

IP_Machine1 = str(sys.argv[2])




context = zmq.Context()

#  Socket to get binary images
socket_pull = context.socket(zmq.PULL)

socket_pull.bind("tcp://127.0.0.1:"+collector1Port)

#socket to send the boxes (contours)

socket_push = context.socket(zmq.PUSH)

socket_push.bind("tcp://"+IP_Machine1+":"+collector1PortPush)
timer = time.monotonic()
while True:
    try:
        msg = socket_pull.recv_json(flags=zmq.NOBLOCK)
        socket_push.send_json(msg)
        timer = time.monotonic()
    except zmq.Again:
        if (time.monotonic() > timer + 300):
            break
print("killed: collector1 number ",collectorNumber)
