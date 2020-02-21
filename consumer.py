from commonfunctions import *

def recv_img(json_obj,socket):
    rec = json.loads(json_obj)

    img = np.asarray(rec["img"])
    return img,rec["title"]


context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5344")


while True:
    msg = socket.recv_json()
    img,title = recv_img(msg,socket)
    io.imsave(title + ".png",img)
