from commonfunctions import *
import sys
import time
collector2Port = str(5800)
context = zmq.Context()

socket = context.socket(zmq.PULL)
print("created: collector2")

socket.bind("tcp://127.0.0.1:"+collector2Port)
file = open('boxex.txt','w')

timer = time.monotonic()

while True:
    try:
        msg = socket.recv(flags=zmq.NOBLOCK)
        print("collector2 rec")
        msg_dict = pickle.loads(msg)
        json.dump(msg_dict,file)
        file.write("\n\n\n")
        timer = time.monotonic()
    except zmq.Again:
        time.sleep(1)
        if (time.monotonic() > timer + 300):
            break
print("killed: collector2")
file.close()