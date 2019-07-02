import ccxt
import datetime

import time

# OK! speed  bitkk ——》bitforex-》 huobiru  ->coinex

exchange = ccxt.allcoin({
    'proxies': {
        'http': 'http://144.202.27.74:8888',  # no auth
        'https': 'https://144.202.27.74:8888',  # no auth
    }})
data = exchange.fetch_ticker('BTC/USDT')
print(data)

# exchange = ccxt.coinex()
# timeStart1 = datetime.datetime.now()
# data = exchange.fetch_ticker('BTC/USDT')
# timeEnd1 = datetime.datetime.now()
# print(data)
# print("iso t: %s" % timeStart1.isoformat())
# print(timeEnd1-timeStart1)


# exchange = ccxt.huobiru()
# print("exchange:",exchange["url"])

# timeStart1 = datetime.datetime.now()
# data = exchange.fetch_ticker('EOS/USDT')
# timeEnd1 = datetime.datetime.now()
# print(data)
# print("iso t:%s" % timeStart1.isoformat())
# print(timeEnd1-timeStart1)


# exchange = ccxt.bitforex()
# timeStart1 = datetime.datetime.now()
# data = exchange.fetch_ticker('BTC/USDT')
# timeEnd1 = datetime.datetime.now()
# print(data)
# print("iso t:%s" % timeStart1.isoformat())
# print(timeEnd1-timeStart1)


# exchange = ccxt.bitkk()
# timeStart1 = datetime.datetime.now()
# data = exchange.fetch_ticker('BTC/USDT')
# timeEnd1 = datetime.datetime.now()
# print(data)
# print("iso t:%s" % timeStart1.isoformat())
# print(timeEnd1-timeStart1)



# exchange2 = ccxt.binance({
#     'proxies': {
#         'http': 'http://127.0.0.1:1080',  # no auth
#         'https': 'https://127.0.0.1:1080',  # with auth
#     }})

# data2 = exchange2.fetch_ticker('BTC/USDT')
# print(data2)