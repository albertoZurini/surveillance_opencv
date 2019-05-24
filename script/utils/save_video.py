from moviepy.editor import *
import cv2
import threading
import gc

class SaveVideo():
  def __init__(self, FPS):
    self.FPS = FPS
    self.frames = []
    self.t = None
    self.clip = None
  
  def add_frame(self, frame, correct=False):
    if correct:
      self.frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    else:
      self.frames.append(frame)
  
  def thread(self, file_name, callback, callback_args):
    self.clip.write_videofile('%s' % file_name, fps=self.FPS)
    del self.frames
    gc.collect()
    self.frames = []
    if callback is not None:
      callback(callback_args[0], callback_args[1])
    print('TERMINATE')
    return

  def close(self, file_name, callback=None, callback_args=None):
    self.clip = ImageSequenceClip(list(self.frames), fps=self.FPS)
    self.t = threading.Thread(target=self.thread, args=(file_name, callback, callback_args,))
    self.t.start()

if __name__ == '__main__':
  import numpy as np
  sv = SaveVideo('a.mp4', 1)
  for i in range(10):
    frame = np.random.randn(720, 1280, 3)
    sv.add_frame(frame)
  sv.close()