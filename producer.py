from commonfunctions import *
#if there still frames return true  with the image else return false
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        return hasFrames,image
        #cv2.imwrite("image"+str(count)+".png", image)     # save frame as JPG file
    return hasFrames, None


def send_img(title,img,socket):
    sent = {
    'img': img.tolist(),
    'title':title
    }
    jobj = json.dumps(sent)
    socket.send_json(jobj)


context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5344")
#read video
vidcap = cv2.VideoCapture('tgf.webm')
li = []
sec = 0
frameRate = 0.2 #//it will capture image in each 0.5 second
count=1
success,img = getFrame(sec)

while success:
    li.append(img)
    send_img(str(count),img,socket)
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success,img = getFrame(sec)
#show_images(li)
print(len(li))





