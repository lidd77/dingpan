# -*- coding: utf-8 -*-

import asyncio
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402


async def run_all_exchanges(exchange_ids):
    results = {}

    for exchange_id in exchange_ids:

        exchange = getattr(ccxt, exchange_id)({
            'enableRateLimit': True,  # required accoding to the Manual
        })

        symbol = 'ETH/BTC'
        print('Exchange:', exchange_id)
        
        try:
            print(exchange_id, 'symbols:')
            markets = await load_markets(exchange, symbol)  # ←----------- STEP 1
            print(list(markets.keys()))

            print(symbol, 'ticker:')
            ticker = await fetch_ticker(exchange, symbol)  # ←------------ STEP 2
            print(ticker)
                
            # print(symbol, 'orderbook:')
            # orderbook = await fetch_orderbook(exchange, symbol)  # ←------ STEP 3
            # print(orderbook)

            await exchange.close()  # ←----------- LAST STEP GOES AFTER ALL CALLS

            results[exchange_id] = ticker
            print(">>> exchange: OK",exchange_id)
        except:
            await exchange.close()  # ←----------- LAST STEP GOES AFTER ALL CALLS
            print(">>> exchange: error",exchange_id)
            continue

    return results


async def load_markets(exchange, symbol):
    try:
        result = await exchange.load_markets()
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        #raise e


async def fetch_ticker(exchange, symbol):
    try:
        result = await exchange.fetch_ticker(symbol)
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        # raise e


async def fetch_orderbook(exchange, symbol):
    try:
        result = await exchange.fetch_order_book(symbol)
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        #raise e


if __name__ == '__main__':
    #exchange_ids = ['bitfinex', 'okex', 'exmo']
    exchange_ids = ccxt.exchanges
    exchanges = []
    results = asyncio.get_event_loop().run_until_complete(run_all_exchanges(exchange_ids))

    print([(exchange_id, ticker) for exchange_id, ticker in results.items()])


'''
exchange:66 OK
 _1btcxe, bequant binanceje bit2c bitbank bitbay bitflyer bitforex bitibu bitkk bitmarket bitso bitstamp bitstamp1
  bittrex bitz bl3p bleutrade btcbox btcchina btcexchange btctradeua buda chbtc chilebit coinbase coinbaseprime
 coinbasepro coincheck coinex coinfloor coinmate coinnest coinone coinspot deribit dsx ethfinex fcoinjp foxbit
 fybse fybsg gdax gemini getbtc hadax huobiru ice3x independentreserve indodax itbit jubi kraken kuna lakebtc
 luno lykke mercado mixcoins negociecoins nova okcoincny paymium quadrigacx southxchange surbitcoin
  '''
''' aviai
  binanceje ,coinbaseprime,huobiru
'''