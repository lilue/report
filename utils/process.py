import time
import datetime
import re


def process_date(date):
    try:
        timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(str(e))
        timeArray = time.strptime(date, "%Y/%m/%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    time_local = time.localtime(timeStamp)
    try:
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        dtArray = dt.split(' ', 1)
        folder = dtArray[0].replace('-', '')
    except Exception as ex:
        print(str(ex))
        dt = time.strftime("%Y/%m/%d %H:%M:%S", time_local)
        dtArray = dt.split(' ', 1)
        folder = dtArray[0].replace('/', '')
    # list_folder = list(folder)
    # if len(folder) == 7:
    #     list_folder.insert(4, '0')
    #     folder = ''.join(list_folder)
    # elif len(folder) == 6:
    #     list_folder.insert(4, '0')
    #     list_folder.insert(6, '0')
    #     folder = ''.join(list_folder)
    return folder


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

