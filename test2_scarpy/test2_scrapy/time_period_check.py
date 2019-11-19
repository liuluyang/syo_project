import time


created_at = '2018-09-05 10:'
updated_at = '2018-09-05 11:56:23'


def time_period_check(created_at, updated_at, period=300):
    format_list = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
    timestamps_c = time.time()
    for f in format_list:
        try:
            timestamps_c = int(
                time.mktime(time.strptime(created_at, f)))
            break
        except:
            pass
    timestamps_u = int(
        time.mktime(time.strptime(updated_at, "%Y-%m-%d %H:%M:%S")))
    if timestamps_u-timestamps_c<period:
        return True
    return False

if __name__ == '__main__':
    print (time_period_check(created_at, updated_at))
