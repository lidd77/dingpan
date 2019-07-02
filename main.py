#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests;
import json;
import asyncio
import types
from configparser import ConfigParser
#import websockets
import websocket
import dateutil.parser as dp
import hmac
import base64
import zlib

#log config
import logging
import logging.handlers
import logging.config
from datetime import datetime

symbol1LastCallTime  = 0.0 
symbol2LastCallTime  = 0.0 
symbol3LastCallTime  = 0.0 

api_key = '78e83f11-0fc6-41ba-bb60-8c9042dae10f'
seceret_key = '9F9E3F62F577C6C34FD73540044C4B15'
passphrase = '857824'
url = 'wss://real.okex.com:10442/ws/v3'
channels = ["swap/ticker:BTC-USD-SWAP"]
channel2 = ["spot/ticker:BTC-USDT","spot/ticker:ETH-USDT","spot/ticker:EOS-USDT"]

class cfgSet:
    pass

cfgSet = cfgSet()

def loginParams(ws):
    unixTime = time.time()
    timestamp = str(round(unixTime))
    message = timestamp + 'GET' + '/users/self/verify'
    mac = hmac.new(bytes(seceret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    sign = base64.b64encode(d)
    login_param = {"op": "login", "args": [api_key, passphrase, timestamp, sign.decode("utf-8")]}
    login_str = json.dumps(login_param)
    ws.send(login_str)

def on_message(ws, message):  # 服务器有数据更新时，主动推送过来的数据
    decompress = zlib.decompressobj(-zlib.MAX_WBITS) # see above
    inflated = decompress.decompress(message)
    inflated += decompress.flush()
    # t = tpye(inflated)
    data = str(inflated,encoding='utf-8')
    ticker = json.loads(data)
    logging.info(ticker)
    if 'data' not in ticker:
        return

    try: 
        num = len(ticker['data'])
        i = 0
        while i < num:
            dataCheck(ticker['data'][i]['instrument_id'],ticker['data'][0])
            logging.info(ticker['data'][i]['timestamp'])
            i = i+1
    except Exception as e:
        print("error ",str(e))
        logging.error("error ",str(e))

def on_error(ws, error):  # 程序报错时，就会触发on_error事件
    print("on_error",str(error))
    logging.error("on_error",str(error))

def on_close(ws):
    logging.info("Connection closed ……")
    webSocketRun()

def on_open(ws):  # 连接到服务器之后就会触发on_open事件，这里用于send数据
    loginParams(ws)
    time.sleep(2)
    sub_param = {"op": "subscribe", "args": channel2}
    sub_str = json.dumps(sub_param)
    ws.send(sub_str)

# init
def quoteWatchInit():
    cfg = ConfigParser()
    try:
        cfg.read('config.ini')
        cfg.sections()

        cfgSet.phone = cfg.get('Unity','phone')
        cfgSet.run = cfg.getboolean('Unity','run')
        cfgSet.timeStart = cfg.get('Unity','timeStart')
        cfgSet.timeEnd = cfg.get('Unity','timeEnd')
        logging.info(str(cfgSet.phone)+" "+str(cfgSet.timeStart)+" "+str(cfgSet.timeEnd)+" "+str(cfgSet.run))

        cfgSet.symbol1 = str(cfg.get('pair1','symbol'))
        cfgSet.priceHigh1 = cfg.getfloat('pair1','priceHigh')
        cfgSet.priceLow1 = cfg.getfloat('pair1','priceLow')
        logging.info("pair1: "+str(cfgSet.symbol1)+" "+str(cfgSet.priceHigh1)+" "+str(cfgSet.priceLow1))

        cfgSet.symbol2 = str(cfg.get('pair2','symbol'))
        cfgSet.priceHigh2 = cfg.getfloat('pair2','priceHigh')
        cfgSet.priceLow2 = cfg.getfloat('pair2','priceLow')
        logging.info("pair2: "+str(cfgSet.symbol2)+" "+str(cfgSet.priceHigh2)+" "+str(cfgSet.priceLow2 ))

        cfgSet.symbol3 = str(cfg.get('pair3','symbol'))
        cfgSet.priceHigh3 = cfg.getfloat('pair3','priceHigh')
        cfgSet.priceLow3 = cfg.getfloat('pair3','priceLow')
        logging.info("pair3: "+str(cfgSet.symbol3)+" "+str(cfgSet.priceHigh3)+" "+str(cfgSet.priceLow3))
    except Exception as e:
        logging.error("config error ",str(e))

# check time ,check price 
def dataCheck(symbol,data):
    lastPrice = float(data["last"])
    # check price 
    if symbol == cfgSet.symbol1:
        if lastPrice >= cfgSet.priceHigh1 :
            warnNum = "100001"
        elif lastPrice <= cfgSet.priceLow1:
            warnNum = "100002"
        else:
            return
    elif symbol == cfgSet.symbol2:
        if lastPrice >= cfgSet.priceHigh2 :
            warnNum = "200001"
        elif lastPrice <= cfgSet.priceLow2:
            warnNum = "200002"
        else:
            return
    elif symbol == cfgSet.symbol3:
        if lastPrice >= cfgSet.priceHigh3 :
            warnNum = "300001"
        elif lastPrice <= cfgSet.priceLow3:
            warnNum = "300002"
        else:
            return
    else:
        logging.info("error symbol:",symbol)
    
    #check time
    i = 0
    nowtime = time.time()
    global symbol1LastCallTime,symbol2LastCallTime,symbol3LastCallTime
    if symbol == cfgSet.symbol1:
        if nowtime - symbol1LastCallTime < 3600*2:
            return 
        else:
            symbol1LastCallTime = nowtime
    elif symbol == cfgSet.symbol2:
        if nowtime - symbol2LastCallTime < 3600*2:
            return 
        else:
            symbol2LastCallTime = nowtime
    else:
        if nowtime - symbol3LastCallTime < 3600*2:
            return 
        else:
            symbol3LastCallTime = nowtime

    #check time
    while i < 2:
        rst = sendCall(warnNum)
        i = i+1

# call phone 
def sendCall(warnInfo):
    resp = requests.post(("http://voice-api.luosimao.com/v1/verify.json"),
    auth=("api", "key-1c7411a7ddb9c76d0c739636a715e5f8"),
    data={
	"mobile": cfgSet.phone,
	"code": warnInfo},
    timeout=3 , verify=False)
    result =  json.loads( resp.content )
    logging.info(result)
    return result

def logInit():
    LOG_FORMAT = "%(asctime)s- %(levelname)s - %(message)s [%(filename)s:%(lineno)s]"
    filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")+'.log'
    logging.basicConfig(filename=filename1, level=logging.INFO, format=LOG_FORMAT)

def webSocketRun():
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=15)
    logging.info("webSocketRun")

if __name__ == "__main__":
    websocket.enableTrace(True)
    logInit()
    quoteWatchInit()
    webSocketRun()



'''
#import ccxt
#import ccxt.async_support as ccxt # link against the asynchronous version of ccxt
# log and email
async def quoteWatch():
    print("in quoteWatch")
    tasks = []
    for symbol in cfgSet.symbols:
        tasks.append(getQuote(symbol))
    await asyncio.gather(*tasks)
    time.sleep(1)
# get quote
async def getQuote(symbol) :
    while True:
        print(">>> query symbol:",symbol,datetime.datetime.now())
        ticker = await exchange.fetch_ticker(symbol)
        # check
        dataCheck(symbol,ticker)

        print ("get",ticker["symbol"])
        time.sleep(6)
    return ticker
if __name__ == "__main__":
    quoteWatchInit()
    # quoteWatch()
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(quoteWatch())
    coro = quoteWatch()
    asyncio.ensure_future(coro)
    loop.run_forever()
    exchange.close()

async def load_markets(exchange, symbol):
    try:
        result = await exchange.load_markets()
        return result
    except ccxt.BaseError as e:
        print(type(e).__name__, str(e), str(e.args))
        raise e
exchange = ccxt.huobiru({
            'apiKey':"afwo04df3f-15525462-823e2387-4e62e",
            'enableRateLimit': True,  # required accoding to the Manual
        })
print("rateLimit:",exchange.rateLimit)


# markets = await exchange.load_markets()
# print (markets)
'''