#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests;
import json;
#import configparser
from configparser import ConfigParser,ExtendedInterpolation
import websocket
import hmac
import base64
import zlib

#log config
import logging
from datetime import datetime

import unittest
from huobi.impl.websocketrequestimpl import WebsocketRequestImpl
from huobi.model import *
from huobi.impl.utils import *
from huobi.model import *
from tests.mock_websocket_connection import MockWebsocketConnection
from huobi.impl.utils.timeservice import convert_cst_in_millisecond_to_utc

symbol1LastCallTime  = 0.0 
symbol2LastCallTime  = 0.0 
symbol3LastCallTime  = 0.0 
symbol4LastCallTime  = 0.0 


# REST API
# https://api.huobi.pro
# Websocket Feed（行情）
# wss://api.huobi.pro/ws

# Websocket Feed（资产和订单）
# wss://api.huobi.pro/ws/v1


url = 'wss://api.huobi.pro/ws'
acessKey =   '47336ebb-db083389-vf25treb80-ef994'
SecretKey = '467db9e7-9228ac9d-3e31942a-6f89b'

class cfgSet:
    pass

cfgSet = cfgSet()


def init():
  subscription_client = SubscriptionClient(api_key=acessKey, secret_key=SecretKey)
  subscription_client.subscribe_trade_event("btcusdt", callback)

  def callback(trade_event: 'TradeEvent'):
    print(trade_event.symbol)
    for trade in trade_event.trade_list:
        print(trade.price)

def loginParams(ws):
    unixTime = time.time()
    timestamp = str(round(unixTime))
    message = timestamp + 'GET' + '/users/self/verify'
    mac = hmac.new(bytes(cfgSet.seceret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    sign = base64.b64encode(d)
    login_param = {"op": "login", "args": [cfgSet.api_key, cfgSet.passphrase, timestamp, sign.decode("utf-8")]}
    login_str = json.dumps(login_param)
    ws.send(login_str)

def on_message(ws, message):  # 服务器有数据更新时，主动推送过来的数据
    decompress = zlib.decompressobj(-zlib.MAX_WBITS) # see above
    inflated = decompress.decompress(message)
    inflated += decompress.flush()
    data = str(inflated,encoding='utf-8')
    ticker = json.loads(data)
    logging.info(ticker)
    if 'data' not in ticker:
        print(ticker)
        return
    num = len(ticker['data'])
    i = 0
    try: 
        while i < num:
            dataCheck(ticker['data'][i]['instrument_id'],ticker['data'][0])
            #logging.info(ticker['data'][i]['timestamp'])
            i = i+1
    except Exception as e:
        print("error ",str(e))
        logging.error(str(e))

def on_error(ws, error):  # 程序报错时，就会触发on_error事件
    print("on_error",str(error))
    logging.error("on_error",str(error))

def on_close(ws):
    logging.info("Connection closed ……")
    print("Connection closed ……")
    time.sleep(60)
    logging.info("Connection restart!")
    webSocketRun()

def on_open(ws):  # 连接到服务器之后就会触发on_open事件，这里用于send数据
    loginParams(ws)
    time.sleep(2)
    sub_param = {"op": "subscribe", "args":cfgSet.subscribe}
    sub_str = json.dumps(sub_param)
    ws.send(sub_str)

def quoteWatchInit():
    print("in quoteWatchInit\r\n")
    #cfg = ConfigParser()
    cfg =  ConfigParser(interpolation=ExtendedInterpolation())
    try:
        cfg.read('./config.ini')
        cfg.sections()

        cfgSet.api_key = str(cfg.get('Unity','api_key'))
        cfgSet.seceret_key = str(cfg.get('Unity','seceret_key'))
        cfgSet.passphrase = str(cfg.get('Unity','passphrase'))
        print(cfgSet.api_key+","+cfgSet.seceret_key+","+cfgSet.passphrase)
        logging.info(cfgSet.api_key+","+cfgSet.seceret_key+","+cfgSet.passphrase)
        cfgSet.phoneKey = str(cfg.get('Unity','phoneKey'))
        print(cfgSet.phoneKey)
        logging.info(cfgSet.phoneKey)

        cfgSet.phone = cfg.get('Unity','phone')
        channel = cfg.get('Unity','subscribe')
        cfgSet.subscribe = channel.split(',')
        logging.info(cfgSet.subscribe)
        print(cfgSet.subscribe)
        logging.info(str(cfgSet.phone))

        cfgSet.symbol1 = str(cfg.get('pair1','symbol'))
        cfgSet.priceHigh1 = cfg.getfloat('pair1','priceHigh')
        cfgSet.priceLow1 = cfg.getfloat('pair1','priceLow')
        logging.info("pair1: "+str(cfgSet.symbol1)+" "+str(cfgSet.priceHigh1)+" "+str(cfgSet.priceLow1))
        print(("pair1: "+str(cfgSet.symbol1)+" "+str(cfgSet.priceHigh1)+" "+str(cfgSet.priceLow1)))

        cfgSet.symbol2 = str(cfg.get('pair2','symbol'))
        cfgSet.priceHigh2 = cfg.getfloat('pair2','priceHigh')
        cfgSet.priceLow2 = cfg.getfloat('pair2','priceLow')
        logging.info("pair2: "+str(cfgSet.symbol2)+" "+str(cfgSet.priceHigh2)+" "+str(cfgSet.priceLow2 ))
        print("pair2: "+str(cfgSet.symbol2)+" "+str(cfgSet.priceHigh2)+" "+str(cfgSet.priceLow2 ))

        cfgSet.symbol3 = str(cfg.get('pair3','symbol'))
        cfgSet.priceHigh3 = cfg.getfloat('pair3','priceHigh')
        cfgSet.priceLow3 = cfg.getfloat('pair3','priceLow')
        logging.info("pair3: "+str(cfgSet.symbol3)+" "+str(cfgSet.priceHigh3)+" "+str(cfgSet.priceLow3))
        print("pair3: "+str(cfgSet.symbol3)+" "+str(cfgSet.priceHigh3)+" "+str(cfgSet.priceLow3))

        cfgSet.symbol4 = str(cfg.get('pair4','symbol'))
        cfgSet.priceHigh4 = cfg.getfloat('pair4','priceHigh')
        cfgSet.priceLow4 = cfg.getfloat('pair4','priceLow')

        logging.info("pair4: "+str(cfgSet.symbol4)+" "+str(cfgSet.priceHigh4)+" "+str(cfgSet.priceLow4))
        print("pair4: "+str(cfgSet.symbol4)+" "+str(cfgSet.priceHigh4)+" "+str(cfgSet.priceLow4))
    except Exception as e:
        logging.error("config error ",str(e))
        print("config error ",str(e))
# check time ,check price 
def dataCheck(symbol,data):

    try:
        lastPrice = float(data["last"])
    except Exception as e:
        print("error ",str(e))
        logging.info("error ",str(e))

    # check price 
    if symbol == cfgSet.symbol1:
        if lastPrice > cfgSet.priceHigh1 :
            warnNum = "100001"
        elif lastPrice < cfgSet.priceLow1:
            warnNum = "100002"
        else:
            return
    elif symbol == cfgSet.symbol2:
        if lastPrice > cfgSet.priceHigh2 :
            warnNum = "200001"
        elif lastPrice < cfgSet.priceLow2:
            warnNum = "200002"
        else:
            return
    elif symbol == cfgSet.symbol3:
        if lastPrice > cfgSet.priceHigh3 :
            warnNum = "300001"
        elif lastPrice < cfgSet.priceLow3:
            warnNum = "300002"
        else:
            return
    elif symbol == cfgSet.symbol4:
        if lastPrice > cfgSet.priceHigh4 :
            warnNum = "400001"
        elif lastPrice < cfgSet.priceLow4:
            warnNum = "400002"
        else:
            return
    else:
        logging.info("error symbol:",symbol)
        print("error symbol:",symbol)
    
    #check time
    i = 0
    nowtime = time.time()
    global symbol1LastCallTime,symbol2LastCallTime,symbol3LastCallTime,symbol4LastCallTime
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
    elif symbol == cfgSet.symbol3:
        if nowtime - symbol3LastCallTime < 3600*2:
            return 
        else:
            symbol3LastCallTime = nowtime
    else:
        if nowtime - symbol4LastCallTime < 3600*2:
            return 
        else:
            symbol4LastCallTime = nowtime
        

    #check time
    while i < 2:
        rst = sendCall(warnNum)
        if rst['error'] == 0:
            i = i+1
        elif rst['error'] == -99999:
            pass
        time.sleep(61)

# call phone
def sendCall(warnInfo):

    try:
        resp = requests.post(("http://voice-api.luosimao.com/v1/verify.json"),
        auth=("api", cfgSet.phoneKey),
        data={
        "mobile": cfgSet.phone,
        "code": warnInfo},
        timeout=10 , verify=False)
        result =  json.loads( resp.content )
    except Exception as e:
        logging.error("config error ",str(e))
        result = {
            'error': -99999
        }
        json_str = json.dumps(result)
        print(json_str)
    print("call "+cfgSet.phone+" :"+warnInfo)
    logging.info("call "+cfgSet.phone+" :"+warnInfo)
    logging.info(result)
    print(result)
    return result

def logInit():
    LOG_FORMAT = "%(asctime)s- %(levelname)s - %(message)s [%(filename)s:%(lineno)s]"
    filename = datetime.now().strftime("%Y%m%d-%H%M%S")+'.log'
    logging.basicConfig(filename="./logs/"+filename, level=logging.INFO, format=LOG_FORMAT)
    print("create ./logs/",filename)

def webSocketRun():
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=15)
    logging.info("webSocketRun")
    print("webSocket Runing ....")

if __name__ == "__main__":
  init()
    # websocket.enableTrace(True)
    # logInit()
    # quoteWatchInit()
    # webSocketRun()
