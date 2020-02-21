from commonfunctions import *
import sys
import math
import time
consumerNumber = int(sys.argv[1])
collector1Port = 5400 + math.ceil(consumerNumber/2.0)
print(consumerNumber)
def recv_img(json_obj):
    rec = json.loads(json_obj)

    img = np.asarray(rec["img"],dtype=np.uint8)
    return img,rec["title"]
def send_img(title,img,socket):
    #img = img.astype(np.uint8)
    sent = {
    'img': img.tolist(),
    'title':title
    }
    jobj = json.dumps(sent)
    socket.send_json(jobj)

context = zmq.Context()

#  Socket to talk to server
socketPull = context.socket(zmq.PULL)
socketPush = context.socket(zmq.PUSH)

socketPull.connect("tcp://127.0.0.1:5333")
socketPush.connect("tcp://127.0.0.1:"+str(collector1Port))

timer = time.monotonic()
while True:
    
    try:
        msg = socketPull.recv_json(flags=zmq.NOBLOCK)
        timer = time.monotonic()
        img,title = recv_img(msg)
        img = rgb2gray(img)
        T = threshold_otsu(img)
        binary = np.vectorize(lambda x: (255) if x>T else 0)
        img = binary(img)
        # io.imsave(title+" from consumer "+str(consumerNumber) + ".png",img)
        send_img(title,img,socketPush)
        timer = time.monotonic()
    except zmq.Again:
        if (time.monotonic() > timer + 10):
            break

