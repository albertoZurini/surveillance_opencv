from darknet import *
import cv2
import time

net = load_net(b"cfg/yolov3-tiny.cfg", b"weights/yolov3-tiny.weights", 0)
meta = load_meta(b"cfg/coco.data")

#r = detect(net, meta, b"img/traffic-hotspots.jpg")
#img = cv2.imread('img/traffic-hotspots.jpg')

cap = cv2.VideoCapture(0)

while True:
  ret, img = cap.read()
  if ret == False:
    print("ERROR")
    break
  r = detect(net, meta, img)
  print(r)

  for detection in r:
    class_name = detection[0].decode("utf-8")
    accuracy = detection[1]
    (cx, cy, w, h) = detection[2]
    x1 = cx - w/2
    x2 = cx + w/2
    y1 = cy - h/2
    y2 = cy + h/2
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    img = cv2.putText(img, class_name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

  #cv2.imwrite('yolo3.jpg', img)
  cv2.imshow('img', img)
  if cv2.waitKey(1) & 0xFF == 27:
    break

cv2.destroyAllWindows()