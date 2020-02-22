from commonfunctions import *
import sys
consumerNumber = int(sys.argv[1])
collector1Port = 5600 + math.ceil(consumerNumber/2.0)
collector2Port = 5800 + math.ceil(consumerNumber/2.0)
IP_Machine1 = str(sys.argv[2])



def recv_img(json_obj):
    rec = json.loads(json_obj)

    img = np.asarray(rec["img"],dtype=np.uint8)
    return img,rec["title"]

def get_contours(img):
    image = np.copy(img)
    closed = binary_closing(image)
    bounding_boxes = find_contours(closed,0.8)
    boxes = []
    for box in bounding_boxes:
        boxes.append(box.tolist())
    return boxes

def send_boxes(title,boxes,socket):
    sent = {
        "title": title,
        "boxes": boxes,
        "count": len(boxes)
    }
    j_obj = json.dumps(sent)
    socket.send_json(j_obj)



context = zmq.Context()

#  Socket to get binary images
socket_pull = context.socket(zmq.PULL)

socket_pull.connect("tcp://"+IP_Machine1+":"+str(collector1Port))

#socket to send the boxes (contours)

socket_push = context.socket(zmq.PUSH)

socket_push.connect("tcp://127.0.0.1:"+str(collector2Port))




timer = time.monotonic()

while True:
    try:
        msg = socket_pull.recv_json(flags=zmq.NOBLOCK)
        img,title = recv_img(msg)
        boxes = get_contours(img)
        send_boxes(title,boxes,socket_push)
        print(len(boxes))
    except zmq.Again:
        if (time.monotonic() > timer + 120):
            break
