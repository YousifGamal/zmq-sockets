from commonfunctions import *
import sys
import time
collectorNumber = int(sys.argv[1])
collector2Port = str(5800 + collectorNumber)
context = zmq.Context()

socket = context.socket(zmq.PULL)

socket.bind("tcp://127.0.0.1:"+collector2Port)
file = open('boxex.txt','w')

timer = time.monotonic()

while True:
    try:
        msg = socket.recv_json(flags=zmq.NOBLOCK)
        msg_dict = json.loads(msg)
        json.dump(msg_dict,file)
        file.write("\n\n\n")
        timer = time.monotonic()
    except zmq.Again:
        if (time.monotonic() > timer + 200):
            break

file.close()