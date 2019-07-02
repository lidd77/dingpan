import os
import sys
import time

# ------------------------------------------------------------------------------

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

# ------------------------------------------------------------------------------

import ccxt  # noqa: E402

# ------------------------------------------------------------------------------

exchange = ccxt.okex({
    'proxies': {
        'http': 'http://127.0.0.1:1080',  # no auth
        'https': 'https://127.0.0.1:1080',  # with auth
    },
    'apiKey': '78e83f11-0fc6-41ba-bb60-8c9042dae10f',
    'secret': '9F9E3F62F577C6C34FD73540044C4B15',
    'enableRateLimit': True,
})
exchange.load_markets()
tickerFile = open("ticker.txt","w")

for symbol in exchange.markets:
    market = exchange.markets[symbol]
    if market['future']:
        print('----------------------------------------------------')
        data = exchange.fetchTicker(symbol)
        print(symbol, data)
        tickerFile.write('\r\n----------------------------------------------------\r\n')
        tickerFile.write(str(data))
        time.sleep(exchange.rateLimit / 20000)

tickerFile.close()

print(ccxt.bitfinex().fetch_ticker('BTC/USDT'))
