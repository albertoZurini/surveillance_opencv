import cv2
import vimeo
import time
import sys
sys.path.append('..')
from utils import notification
from utils import configuration

# https://developer.vimeo.com/api/upload/videos
CLIENT_IDENTIFIER = configuration.VIMEO_CLIENT_IDENTIFIER
CLIENT_SECRET = configuration.VIMEO_CLIENT_SECRET
TOKEN = configuration.VIMEO_TOKEN
THE_NEXT_IS_TRIGGERED = False

def upload(name, file_name, description='recording', password='zurini'):
  global CLIENT_IDENTIFIER, CLIENT_SECRET, TOKEN, net, meta, THE_NEXT_IS_TRIGGERED

  if not THE_NEXT_IS_TRIGGERED:
    print('Not uploading')
    return

  client = vimeo.VimeoClient(
    token=TOKEN,
    key=CLIENT_IDENTIFIER,
    secret=CLIENT_SECRET
  )
  #file_name = '../recordings/25_04_2019-13:38:35.mp4'
  uri = client.upload(file_name, data={
    'name': name,
    'description': description
  })

  print('Your video URI is: %s' % (uri))

  while True:
    response = client.get(uri + '?fields=transcode.status').json()
    if response['transcode']['status'] == 'complete':
      print('Your video finished transcoding.')
      break
    elif response['transcode']['status'] == 'in_progress':
      print('Your video is still transcoding.')
    else:
      print('Your video encountered an error during transcoding.')
      quit()
    time.sleep(5)

  response = client.get(uri + '?fields=link').json()
  print('Video link: %s' % response['link'])

  client.patch(uri, data={
    'privacy': {
      'view': 'password'
    },
    'password': password
  })
  client.patch(uri, data={
    'privacy': {
      'embed': 'private'
    }
  })

  notification.send_message('Video uploaded. URL: %s' % response['link'])
  THE_NEXT_IS_TRIGGERED = False

if __name__ == '__main__':
  upload('a', '../recordings/15_05_2019-09:44:07.mp4')
