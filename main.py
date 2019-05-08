import numpy as np
import time
import os
import cv2
import threading
import imageio
import gc

from utils import img_diff
from utils import img_text
from utils import notification
from utils import delete_older
from utils import save_video
import configuration

RTSP_URL = configuration.CAM_URL
STDEV_TRESH = configuration.STDEV_TRESH

if not os.path.exists(configuration.RECORDINGS_PATH):
    os.makedirs(configuration.RECORDINGS_PATH)

cap = cv2.VideoCapture(configuration.CAM_URL)
old_frame = None
current_time_counter = 0
time_per_recording = configuration.MAX_TIME_RECORDNG # seconds
video_arr = []
recordingStarted = False

#cap = imageio.get_reader('<video0>')

ret, frame = cap.read()

#frame = cap.get_next_data()
#frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

frame_height, frame_width, _ = frame.shape

FPS = 10
'''
count = 0
print('Calculating FPS...', end=' ')
for i in range(30):
  start = time.time()
  #frame = cap.get_next_data()
  #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  ret, frame = cap.read()
  end = time.time()
  nowFps = 1/(end-start)
  FPS += nowFps
  count += 1
FPS = int(FPS/count)
print('| FPS: ', FPS)
'''
out = save_video.SaveVideo(FPS)
  
while True:
  #frame = cap.get_next_data()
  #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  ret, frame = cap.read()

  if ret == False:
    print('error')
    break
    
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

  if old_frame is None:
    old_frame = frame
  else:
    occ = img_diff.occupied(old_frame, frame)
    #if configuration.DEBUG_STDEV == True:
    #  print(occ)
    
    t = time.strftime('%d/%m/%Y %H:%M:%S')
    frame2 = img_text.putTextWithBackground(frame, t)
    frame2 = img_text.putTextWithBackground(frame2, str(int(occ[0][0]*10)/10), offset=1230)
    if configuration.CLI == False:
      cv2.imshow('frame', frame2)

    if occ > STDEV_TRESH: # if the zone is being occupied
      #print('occupied')
      #notification.maybe_send(frame, configuration.ALERT_URL, TIMEOUT=configuration.ALERT_TIMEOUT)
      if not recordingStarted and time.time() - current_time_counter > time_per_recording:
        current_time_counter = time.time() # reset the timer to current time
    
    if time.time() - current_time_counter < time_per_recording:
      #print('Recording...')
      #out.write(frame2)
      out.add_frame(frame2, True)
      recordingStarted = True
    else:
      if recordingStarted == True:
        out.close('%s/%s.mp4' % (configuration.RECORDINGS_PATH, time.strftime('%d_%m_%Y-%H:%M:%S')))
        print('RELEASE')
        recordingStarted = False
        delete_older.delete(configuration.RECORDINGS_PATH, configuration.DELETE_VIDEO_AFTER)

    old_frame = frame

cap.release()
#cap.close()