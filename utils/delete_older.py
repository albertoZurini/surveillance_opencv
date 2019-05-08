import os
import time
import datetime

def delete(path, maxTime):
  for fn in os.listdir(path):
    timestamp = time.mktime(datetime.datetime.strptime(fn.split('.')[0], '%d_%m_%Y-%H:%M:%S').timetuple())
    if time.time() - timestamp > maxTime:
      print('Deleted %s' % fn)
      os.remove(os.path.join(path, fn))


if __name__ == '__main__':
  delete('../recordings', 1*60*60*24)