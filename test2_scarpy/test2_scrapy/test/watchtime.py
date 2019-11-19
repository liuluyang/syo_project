import time
import logging



loger = logging.getLogger()
loger.setLevel(logging.INFO)
l = logging.FileHandler('logging_test.log','a',encoding='utf8')
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
l.setFormatter(formatter)
loger.addHandler(l)

while True:
    t = time.strftime('%Y-%m-%d %X', time.localtime())
    loger.info(t)
    time.sleep(5)
