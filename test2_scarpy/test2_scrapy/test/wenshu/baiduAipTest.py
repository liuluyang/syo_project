# -*- coding: UTF-8 -*-

from aip import AipOcr
import json

# 定义常量
APP_ID = '16209183'
API_KEY = 'DnB2038Qr4H9EzFffOiuHvY9'
SECRET_KEY = 'KFhQ01HO52NihPA41tiIsqxcwlNuR3l6'

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath = "book01.png"


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'ENG',
}

# 调用通用文字识别接口
result = aipOcr.webImage(get_file_content(filePath), options)
#result = json.dumps(result)
print(type(result), result)
for w in result['words_result']:
    print(w['words'])
# for w in result['words_result']:
#     print(w)