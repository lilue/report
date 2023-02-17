import time
import datetime
import re


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
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

