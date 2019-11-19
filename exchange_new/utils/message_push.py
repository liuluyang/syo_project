
import time
import json
import requests
import hashlib
from settings import  production_mode, appkey, app_master_secret, method, url

#测试数据
device_token_test = '9afb205583fd1a176851197c912a6d42982ea1d37e4f7f15694f570ab3c2598a'
message_info_test = {"message_type":1,
                    "market":"Binance",
                    "symbol":"BTC",
                    "currency":"USDT"}
alert_test = {"title": "title",
              "subtitle": "subtitle",
              "body": "body"}

class MessagePush(object):

    def __init__(self, mode=None):
        if mode is None:
            mode = production_mode
        else:
            mode = "true" if mode else "false"
        self.production_mode = mode
        self.appkey = appkey
        self.app_master_secret = app_master_secret
        self.method = method
        self.url = url
        self.params = {'appkey': self.appkey,
                  'timestamp': 1111111111,
                  'device_tokens': '',
                  'type': '',
                  "production_mode": self.production_mode,
                  "payload": {
                      "aps": {  # 苹果必填字段
                          "alert": {  # 当content-available=1时(静默推送)，可选; 否则必填。
                              # 可为JSON类型和字符串类型
                              "title": "title",
                              "subtitle": "subtitle",
                              "body": "body"
                          },
                          "badge": 1,
                          "sound": "true"
                      },
                  },
                  }

    def _md5(self, s):
        m = hashlib.md5(s.encode())
        return m.hexdigest()

    def _send(self, sign, post_body):
        res = requests.post(
            'http://msg.umeng.com/api/send?sign={}'.format(sign),
            data=post_body)

        return res.status_code

    def ios_unicast(self, message_info, alert, device_token=None):
        if isinstance(message_info, dict):
            if not isinstance(message_info.get('message_type'), int):
                return '未设置消息类型'
            self.params['payload']['message_info'] = message_info
        else:
            return 'message_info 参数类型错误'
        if isinstance(alert, dict) and alert.get('title') and alert.get('body'):
            self.params['payload']['aps']['alert'] = alert
        else:
            return 'alert 参数错误'
        self.params['device_tokens'] = device_token if device_token else device_token_test

        self.params['type'] = 'unicast'
        self.params['timestamp'] = int(time.time()*1000)
        post_body = json.dumps(self.params)
        s = '%s%s%s%s' % (self.method, self.url, post_body, self.app_master_secret)
        sign = self._md5(s)
        status_code = self._send(sign, post_body)

        return status_code

if __name__ == '__main__':
    m = MessagePush()
    #print (m.ios_unicast(message_info_test, alert_test))
