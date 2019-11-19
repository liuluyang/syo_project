import time

time_now = '2018-10-31T22:58:00Z'

def bigone_time_change(time_now, is_str=False):
    """
    bigone0时区时间转化为8时区
    :param time_now: 
    :param is_str: 
    :return: timestamp or time_str
    """
    time_utc0 = time_now[:-1]
    time_utc0 = time_utc0.replace('T', ' ')
    time_struct = time.strptime(time_utc0, '%Y-%m-%d %X')
    timestamp = time.mktime(time_struct) + 28800
    if is_str:
        time_new = time.strftime('%Y-%m-%d %X', time.localtime(timestamp))
        return time_new

    return timestamp

print(bigone_time_change(time_now, True))

