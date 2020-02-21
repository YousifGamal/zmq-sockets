from commonfunctions import *

context = zmq.Context()

socket = context.socket(zmq.PULL)

socket.bind("tcp://127.0.0.1:5570")

file = open('boxex.txt','w')
while True:
    msg = socket.recv_json()
    msg_dict = json.loads(msg)
    json.dump(msg_dict,file)
    file.write("\n\n\n")

file.close()