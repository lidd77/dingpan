import hmac
import base64
import requests
import json

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
request_path = '/api/account/v3/currencies'
# set request header
header = get_header('your_api_key', signature('timestamp', 'GET', request_path, 'your_secret_key'), 'timestamp', 'your_passphrase')
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


########################################################
# take order
base_url = 'https://www.okex.com'
request_path = '/api/spot/v3/orders'

# request params
params = {'type': 'market', 'side': 'buy', 'instrument_id': 'usdt_okb', 'size': '10', 'client_oid': '',
                   'price': '10', 'funds': ''}

# request path
request_path = request_path + parse_params_to_str(params)
url = base_url + request_path

# request header and body
header = get_header('your_api_key', signature('timestamp', 'POST', request_path, 'your_secret_key'), 'timestamp', 'your_passphrase')
body = json.dumps(params)

# do request
response = requests.post(url, data=body, headers=header)

#########################################################
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