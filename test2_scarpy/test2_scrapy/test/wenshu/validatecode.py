import requests
import random
from test2_scrapy.test.wenshu.user_agents import agents
from urllib.request import urlretrieve
from PIL import Image, ImageDraw

def clearImg():
    def test(path):
        img = Image.open(path)
        w, h = img.size
        for x in range(w):
            for y in range(h):
                r, g, b = img.getpixel((x, y))
                if 190 <= r <= 255 and 170 <= g <= 255 and 0 <= b <= 140:
                    img.putpixel((x, y), (0, 0, 0))
                if 0 <= r <= 90 and 210 <= g <= 255 and 0 <= b <= 90:
                    img.putpixel((x, y), (0, 0, 0))
        img = img.convert('L').point([0] * 150 + [1] * (256 - 150), '1')
        return img

    test('D:/liuluyang/test2_scarpy/test2_scrapy/test/wenshu/code.jpg').\
        save('D:/liuluyang/test2_scarpy/test2_scrapy/test/wenshu/code.jpg')

    # for i in range(1,13):
    #     path = str(i) + '.jpg'
    #     im = test(path)
    #     path = path.replace('jpg','png')
    #     im.save(path)


    # -*-coding:utf-8-*-


    # coding:utf-8
    import sys, os

    # 二值数组
    t2val = {}

    def twoValue(image, G):
        for y in range(0, image.size[1]):
            for x in range(0, image.size[0]):
                g = image.getpixel((x, y))
                if g > G:
                    t2val[(x, y)] = 1
                else:
                    t2val[(x, y)] = 0

    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
    # G: Integer 图像二值化阀值
    # N: Integer 降噪率 0 <N <8
    # Z: Integer 降噪次数
    # 输出
    #  0：降噪成功
    #  1：降噪失败
    def clearNoise(image, N, Z):
        for i in range(0, Z):
            t2val[(0, 0)] = 1
            t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    nearDots = 0
                    L = t2val[(x, y)]
                    if L == t2val[(x - 1, y - 1)]:
                        nearDots += 1
                    if L == t2val[(x - 1, y)]:
                        nearDots += 1
                    if L == t2val[(x - 1, y + 1)]:
                        nearDots += 1
                    if L == t2val[(x, y - 1)]:
                        nearDots += 1
                    if L == t2val[(x, y + 1)]:
                        nearDots += 1
                    if L == t2val[(x + 1, y - 1)]:
                        nearDots += 1
                    if L == t2val[(x + 1, y)]:
                        nearDots += 1
                    if L == t2val[(x + 1, y + 1)]:
                        nearDots += 1

                    if nearDots < N:
                        t2val[(x, y)] = 1

    def saveImage(filename, size):
        image = Image.new("1", size)
        draw = ImageDraw.Draw(image)

        for x in range(0, size[0]):
            for y in range(0, size[1]):
                draw.point((x, y), t2val[(x, y)])

        image.save(filename)

    # for i in range(1,12):
    #     path =  str(i) + ".png"
    #     image = Image.open(path).convert("L")
    #     twoValue(image, 100)
    #     clearNoise(image, 3, 2)
    #     path1 = str(i) + ".jpeg"
    #     saveImage(path1, image.size)
    path = 'D:/liuluyang/test2_scarpy/test2_scrapy/test/wenshu/code.jpg'
    image = Image.open(path).convert("L")
    twoValue(image, 100)
    clearNoise(image, 3, 2)
    # path1 = str(i) + ".jpeg"
    saveImage(path, image.size)


headers = {
        'User-Agent':random.choice(agents),
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        #'Referer':'http://wenshu.court.gov.cn/List/List?sorttype=1'
    }


def checkCode(code=''):
    data = {
        'ValidateCode':code
    }
    r = requests.post('http://wenshu.court.gov.cn/Content/CheckVisitCode', data=data,
                      headers=headers
                      )

    print(r.status_code)
    print(r.text)

def getCode():

    r = requests.get('http://wenshu.court.gov.cn/User/ValidateCode/5520',
                     headers=headers
                     )
    print(r.status_code)
    print(r.content)
    with open('code.jpg', 'wb') as f:
        f.write(r.content)

def showCode():
    from PIL import Image
    from pytesseract import image_to_string
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    im = Image.open('D:/liuluyang/test2_scarpy/test2_scrapy/test/wenshu/code.jpg')
    print(image_to_string(im))



def showCode_2():
    # 定义常量
    from aip import AipOcr
    import json
    APP_ID = '9851066'
    API_KEY = 'LUGBatgyRGoerR9FZbV4SQYk'
    SECRET_KEY = 'fB2MNz1c2UHLTximFlC4laXPg7CVfyjV'

    # 初始化AipFace对象
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    filePath = "code.jpg"

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 定义参数变量
    options = {
        'detect_direction': 'true',
        'language_type': 'ENG',
    }

    # 调用通用文字识别接口
    result = aipOcr.basicGeneral(get_file_content(filePath), options)
    print(json.dumps(result))

#getCode()
#clearImg()
#showCode()
#showCode_2()


#getCode()
checkCode('vazz')

