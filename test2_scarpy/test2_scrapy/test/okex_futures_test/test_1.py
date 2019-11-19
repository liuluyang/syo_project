import time
import hmac
import base64
import requests
import json
api_key = 'c0eb690b-cfdb-455a-bfae-4df16e1722f0'
secretKey = '21D206DF1EE981A70B6740334FA69D78'

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
base_url = 'https://www.okex.com'
# request_path = '/api/account/v3/currencies'
request_path = '/api/futures/v3/instruments/BTC-USD-181123/open_interest'
# set request header
timestamps = round(time.time(), 3)
header = get_header(api_key, signature(timestamps, 'GET', request_path,'',
                                       secretKey), timestamps,
                                        '123456')
# do request
response = requests.get(base_url + request_path, headers=header)
# json
print(response.json())

# [{
#     "id": "BTC",
#     "name": “Bitcoin”，
#      "deposit": "1",
#      "withdraw": “1”,
#       “withdraw_min”:”0.000001btc”
# }, {
#     "id": "ETH",
#     "name": “Ethereum”,
#     "deposit": "1",
#      "withdraw": “1”，
#      “withdraw_min”:”0.0001eth”
#     }
#  …
# ]