ALERT_URL = 'http://192.168.1.X/sendImage' # URL the image will be uploaded to
ALERT_TIMEOUT = 30 #seconds
MAX_TIME_RECORDNG = 30 #seconds
CAM_URL = 'rtsp://admin:123456@192.168.1.X' # Camera RTSP URL or ID
STDEV_TRESH = 5 # standard deviation treshold (motion detection. The higher the more movement has to be accomplished to trigger)
DEBUG_STDEV = True # print standard deviation values to choose the best one
RECORDINGS_PATH = './recordings' # path of recordings folder