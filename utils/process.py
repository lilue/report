import time
import datetime
import re


def process_date(date):
    timeArray = time.strptime(date, "%Y/%m/%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    time_local = time.localtime(timeStamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    dtArray = dt.split(' ', 1)
    folder = dtArray[0].replace('-', '')
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
    # dd = process_date('2020/7/03')
    # print(dd)
    dd = '2020/11/1 17:04:16'
    res = process_date(dd)
    print(res)

