import hmac
import base64
import requests
import json
import time

apiKey = '146537f4-7692-4821-ad5a-af03c8cca385'
secretKey = '9681E893CC577593280A82FB43B3DD43'
Passphrase = 'lly123456'
timestamp = str(round(time.time(), 3))

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'



# signature
def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


# set request header
def get_header(api_key, sign, timestamp, passphrase):
    header = dict()
    header[CONTENT_TYPE] = APPLICATION_JSON
    header[OK_ACCESS_KEY] = api_key
    header[OK_ACCESS_SIGN] = sign
    header[OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[OK_ACCESS_PASSPHRASE] = passphrase
    return header


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]


# request example
# set the request url
#/api/futures/v3/ BTC-USD-180309 /position
#/api/futures/v3/accounts/eos/leverage
# base_url = 'https://www.okex.me'
# request_path = '/api/futures/v3/EOS-USD-190329/position'
# # set request header
# header = get_header(apiKey, signature(timestamp, 'GET', request_path, '', secretKey), timestamp, Passphrase)
# # do request
# response = requests.get(base_url + request_path, headers=header)
# # json
# print(response.json())


########################################################
# take order
base_url = 'https://www.okex.me'
request_path = '/api/futures/v3/order'

# request params
#1:开多 2:开空 3:平多 4:平空
params = {"client_oid": "lvjiantest20190227","instrument_id":"EOS-USD-190329",
          "type":"3","price":"","size":1,"match_price":"1",
          "leverage":10}

# request path
request_path = request_path + parse_params_to_str(params)
url = base_url + request_path

# request header and body
body = json.dumps(params)
header = get_header(apiKey, signature(timestamp, 'POST', request_path, body, secretKey), timestamp, Passphrase)


# do request
response = requests.post(url, data=body, headers=header)
print(response.status_code == 200)
print(response.json())

#########################################################
"""
# get order info
base_url = 'https://www.okex.com'
request_path = '/api/spot/v3/orders'

params = {'status':'all', 'instrument_id': 'okb_usdt'}

# request path
request_path = request_path + parse_params_to_str(params)
url = base_url + request_path

# request header and body
header = get_header('your_api_key', signature('timestamp', 'GET', request_path, 'your_secret_key'), 'timestamp', 'your_passphrase')

# do request
response = requests.get(url, headers=header)
"""