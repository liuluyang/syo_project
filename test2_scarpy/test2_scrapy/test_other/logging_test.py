import logging

loger = logging.getLogger()
loger.setLevel(logging.INFO)

l = logging.FileHandler('logging_test.log','a',encoding='utf8')
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
l.setFormatter(formatter)
loger.addHandler(l)


loger.warning('这算是一个警告')
loger.info('这是信息')