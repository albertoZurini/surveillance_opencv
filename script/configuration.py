ALERT_URL = 'http://192.168.1.X/sendImage' # URL the image will be uploaded to
ALERT_TIMEOUT = 30 #seconds
MAX_TIME_RECORDNG = 30 #seconds
CAM_URL = 'rtsp://admin:123456@192.168.1.X' # Camera RTSP URL or ID
STDEV_TRESH = 5 # standard deviation treshold (motion detection. The higher the more movement has to be accomplished to trigger)
DEBUG_STDEV = True # print standard deviation values to choose the best one
RECORDINGS_PATH = './recordings' # path of recordings folderer
DELETE_VIDEO_AFTER = 60*60*24 * 5 # seconds
TRIGGER_CLASS_NAME = ['person']
CLI = True
VIMEO_CLIENT_IDENTIFIER = '87d6fce14d8e'
VIMEO_CLIENT_SECRET = '4mwwpSv/AEw'
VIMEO_TOKEN = '34c0cbc0e6'