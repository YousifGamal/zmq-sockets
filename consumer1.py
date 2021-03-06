from commonfunctions import *
import sys
import math
import time
import pickle
consumerNumber = int(sys.argv[1])


collector1Port = 5400 + math.ceil(consumerNumber/2.0)
print("created: consumer1 number ",consumerNumber,collector1Port)

def recv_img(obj):
    rec = pickle.loads(obj)

    img = np.asarray(rec["img"],dtype=np.uint8)
    return img,rec["title"]
def send_img(title,img,socket):
    #img = img.astype(np.uint8)
    sent = {
    'img': img.tolist(),
    'title':title
    }
    obj = pickle.dumps(sent)
    socket.send(obj,copy=False)

context = zmq.Context()

#  Socket to talk to server
socketPull = context.socket(zmq.PULL)
socketPush = context.socket(zmq.PUSH)

socketPull.connect("tcp://127.0.0.1:5333")
socketPush.connect("tcp://127.0.0.1:"+str(collector1Port))
binary = np.vectorize(lambda x,y: (255) if x>y else 0)
timer = time.monotonic()
while True:
    
    try:
        msg = socketPull.recv(flags=zmq.NOBLOCK)
        print("cons1 rec",consumerNumber)
        timer = time.monotonic()
        img,title = recv_img(msg)
        img = rgb2gray(img)
        T = threshold_otsu(img)
        
        img = binary(img,T)
        # io.imsave(title+" from consumer "+str(consumerNumber) + ".png",img)
        send_img(title,img,socketPush)
        timer = time.monotonic()
    except zmq.Again:
        time.sleep(1)
        if (time.monotonic() > timer + 300):
            break
print("killed: consumer1 number ",consumerNumber)

