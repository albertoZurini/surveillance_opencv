import numpy as np
import time
import os
import cv2

from utils import img_diff
from utils import img_text
from utils import notification
import configuration

RTSP_URL = configuration.CAM_URL
STDEV_TRESH = configuration.STDEV_TRESH

if not os.path.exists(configuration.RECORDINGS_PATH):
    os.makedirs(configuration.RECORDINGS_PATH)

cap = cv2.VideoCapture(RTSP_URL)
old_frame = None
current_time_counter = 0
time_per_recording = configuration.MAX_TIME_RECORDNG # seconds
video_arr = []
recordingStarted = False

ret, frame = cap.read()
frame_height, frame_width, _ = frame.shape

FPS = 0
count = 0
print('Calculating FPS...', end=' ')
for i in range(30):
  start = time.time()
  ret, frame = cap.read()
  end = time.time()
  nowFps = 1/(end-start)
  if nowFps < 30:
    FPS += nowFps
    count += 1
FPS = int(FPS/count)
print('| FPS: ', FPS)

out = cv2.VideoWriter('recording.mp4',cv2.VideoWriter_fourcc('H','2','6','4'), FPS, (frame_width,frame_height))

while True:
  ret, frame = cap.read()

  if ret == False:
    print('error')
    break
  else:
    t = time.strftime('%d/%m/%Y %H:%M:%S')
    frame2 = img_text.putTextWithBackground(frame, t)
    cv2.imshow('frame', frame2)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

  if old_frame is None:
    old_frame = frame
  else:
    occ = img_diff.occupied(old_frame, frame)
    if configuration.DEBUG_STDEV == True:
      print(occ)
    if occ > STDEV_TRESH: # if the zone is being occupied
      print('occupied')
      notification.maybe_send(frame, configuration.ALERT_URL, TIMEOUT=configuration.ALERT_TIMEOUT)
      if time.time() - current_time_counter > time_per_recording:
        current_time_counter = time.time() # reset the timer to current time
    
    if time.time() - current_time_counter < time_per_recording:
      print('Recording...')
      out.write(frame2)
      recordingStarted = True
    else:
      if recordingStarted == True:
        print('Saving the video')
        out.release()
        os.rename('./recording.mp4', '%s/%s.mp4' % (configuration.RECORDINGS_PATH, time.strftime('%d_%m_%Y %H:%M:%S'))) # move to recordings folder
        recordingStarted = False

    old_frame = frame

cap.release()