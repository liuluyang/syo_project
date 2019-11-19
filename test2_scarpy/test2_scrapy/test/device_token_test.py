

data = [(str(i),) for i in range(1,600)]

device_list = [d[0] for d in data]
listcast_num = 400
start_index = 0
for i in range(len(data)//listcast_num+1):
    device_token = ','.join(device_list[start_index:start_index+listcast_num])
    start_index += listcast_num

