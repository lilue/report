import time
# import datetime
import re
from datetime import datetime
from dateutil import parser


def process_date1(date):
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
    return folder


def process_date(temp):
    date = re.sub("星期一|星期二|星期三|星期四|星期五|星期六|星期日|星期天", "", temp)
    date_formats = ["%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %A %H:%M:%S"]
    for date_format in date_formats:
        try:
            time_struct = time.strptime(date, date_format)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Unrecognized date format: {date}")
    print(time_struct)
    time_stamp = int(time.mktime(time_struct))
    print(time_stamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
    print(dt)
    folder = dt.split(' ', 1)[0].replace('-', '').replace('/', '')
    return folder


if __name__ == '__main__':
    str = "2023/2/13 星期一 20:00:00"
    # str = re.sub("星期一|星期二|星期三|星期四|星期五|星期六|星期日|星期天", "", str)
    # print(str)
    dateStr = '2023-2-13 20:00:00'
    dt1 = process_date(str)
    print(dt1)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
