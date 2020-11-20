import datetime
import time

# 时间戳
import pytz

time_stamp = time.time()
print(time_stamp)

# 结构化时间
time_struct = time.localtime()
print(time_struct)

# 格式化时间


time_struct = time.localtime(time_stamp)  # 首先把时间戳转换为结构化时间
time_format = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)  # 把结构化时间转换为格式化时间
print(time_format)

time_format = datetime.datetime.fromtimestamp(time_stamp)  # 直接传入时间戳格式时间
print(time_format)


def utc_to_local(utc_time_str, local_format="%Y-%m-%d %H:%M:%S", utc_format=f'%Y-%m-%dT%H:%M:%S'):
    utc_time_str = utc_time_str[:-8]
    local_tz = pytz.timezone('Asia/Shanghai')
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    ltime = time.localtime(int(time.mktime(time.strptime(time_str, local_format))))
    return time.strftime(local_format, ltime)


current_time_int = utc_to_local('2020-11-13T03:45:17.750064Z')
print(current_time_int)
