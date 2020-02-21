from commonfunctions import *

def recv_img(json_obj,socket):
    rec = json.loads(json_obj)

    img = np.asarray(rec["img"],dtype=np.uint8)
    return img,rec["title"]


context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.PULL)
socket.connect("tcp://10.8.0.10:5333")


while True:
    msg = socket.recv_json()
    img,title = recv_img(msg,socket)
    img = rgb2gray(img)
    io.imsave(title + ".png",img)
