import base64
import gzip
import json

data = 'H4sIAAAAAAAAA4uuVirJzE1VsjI0NTE0MDM0NjMAAh2l/ILUPCUrJQM9ENfUyNxCSUcpIz' \
       'M9A10sJ78cXSg5J784FV2wLD8HJKRUq4NmoYkRVgstTDEtBIuhWggWQrcQLAix0NDMUs/' \
       'A0MDEyMRCqTYWABwzCLLtAAAA'

data_trade = 'H4sIAAAAAAAAA62Su24CMRAA/2Vr67Qvr9dXBv4AqFAUoZDCBQniUSH+HTeIu4gT' \
             'Lmgta8fj2fUF9ptygB4+lrOv1WK+hACnsvuBnqISsQrn7DHA/lC+66mpYqeCHmCz' \
             '+zv/nqDHLrqjqKQAx7KtlzhA2dYJmDhG5XQNrzGCbDrGCCUaYohyfQzfKTSiCLZR' \
             'Eg1lJHdmLEMKi0fzh8w/TG7D5JTGMojZhhjU5M8R2mTSkEWNaCKJvSlJzW7PLbj' \
             'xo172kDpuooW/q4XXtcoTNej6eQN06AXNJgMAAA=='


def inflate(data):
    """
    解压数据
    :param data: 
    :return: 
    """
    data = base64.b64decode(data)
    data = gzip.decompress(data)
    data = json.loads(data.decode())

    return data

print(inflate(data))