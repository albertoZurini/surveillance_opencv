# see https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594
import requests
import json
import cv2
import time
import threading

def send(img, URL):
  _, img_encoded = cv2.imencode('.jpg', img)
  files = {'file': img_encoded}
  print('uploading image...')
  response = requests.post(URL, files=files)
  print(response)

last_time = 0
def maybe_send(image, URL, TIMEOUT=30):
  global last_time, send
  if time.time() - last_time > TIMEOUT:
    last_time = time.time()
    t = threading.Thread(target=send, args=(image, URL,))
    t.start()