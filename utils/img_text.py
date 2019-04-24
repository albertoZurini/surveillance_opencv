import numpy as np
import cv2

def putTextWithBackground(frame, text, offset=0, text_size=1, thickness=2):
  size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, text_size, thickness)
  text_width = size[0][0]
  text_height = size[0][1]
  frame2 = cv2.rectangle(frame.copy(), (offset,0), (offset+text_width,text_height+10), (255,255,255), cv2.FILLED)
  frame2 = cv2.putText(frame2,text,(offset,size[0][1]+5),cv2.FONT_HERSHEY_SIMPLEX, text_size, (0,0,0), thickness)
  return frame2