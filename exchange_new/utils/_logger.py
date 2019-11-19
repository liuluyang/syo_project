import logging
import os

class MakeLogger(object):
    def __init__(self, name='exchange.log'):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, name)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.WARNING)
        l = logging.FileHandler(path, 'a', encoding='utf8')
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        l.setFormatter(formatter)
        self.logger.addHandler(l)


Logger = MakeLogger().logger