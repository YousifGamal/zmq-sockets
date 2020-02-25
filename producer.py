from commonfunctions import *
import cv2
import sys
videoName = sys.argv[1]
#if there still frames return true  with the image else return false
print("created: producer")
cap = cv2.VideoCapture(videoName)
if (cap.isOpened()== False): 
  print("Error opening video stream or file")


def getFrame():
    global cap
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            return ret, frame;
        return ret, None
    else:
        print("error")
        return False, None
    # hasFrames,image = vidcap.read()
    # if hasFrames:
    #     return hasFrames,image
    #     #cv2.imwrite("image"+str(count)+".png", image)     # save frame as JPG file
    # return hasFrames, None


def send_img(title,img,socket):
    #img = img.astype(np.uint8)
    sent = {
    'img': img.tolist(),
    'title':title
    }
    obj = pickle.dumps(sent)
    socket.send(obj,copy=False)

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://127.0.0.1:5333")
#read video
# vidcap = cv2.VideoCapture(videoName)
li = []
count=1
success,img = getFrame()

while success:
    li.append(img)
    send_img(str(count),img,socket)
    print("produced " + str(count))
    count = count + 1
    success,img = getFrame()
#show_images(li)
timer = time.monotonic()

cap.release()
print("killed: producer")
