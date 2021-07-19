# -*- coding: utf-8 -*-
import errno
import json
import logging
import logging.handlers
import os
import time
from configparser import ConfigParser, ExtendedInterpolation

import requests
import websocket

symbol1LastCallTime  = 0.0 
symbol2LastCallTime  = 0.0 
symbol3LastCallTime  = 0.0 
symbol4LastCallTime  = 0.0 

def logInitNew():
    try:
        os.makedirs("./logs", exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs("./logs")
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir("./logs"):
                pass
            else:
                raise


    logger = logging.getLogger(__file__)
    logger.setLevel(logging.INFO)
    #logger =  logging.getLogger("asyncio").setLevel(logging.INFO)

    logHandler = logging.handlers.TimedRotatingFileHandler(
        filename="./logs/log", when='D', interval=1, backupCount=3, encoding='utf-8')

    LOG_FORMAT1 = "%(asctime)s- %(levelname)s - %(message)s [%(filename)s:%(lineno)s]"
    #LOG_FORMAT1 = "%(message)s [%(filename)s:%(lineno)s]"
    logFormatter = logging.Formatter(LOG_FORMAT1)
    logHandler.setFormatter(logFormatter)

    if not logger.handlers:
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s- %(message)s')
        streamhandler.setFormatter(formatter)
        logger.addHandler(streamhandler)
        logger.addHandler(logHandler)

    return logger

log = logInitNew()
url = 'wss://ws.okex.com:8443/ws/v5/public'

class cfgSet:
    pass

cfgSet = cfgSet()


# init
def quoteWatchInit():
    print("in quoteWatchInit\r\n")
    #cfg = ConfigParser()
    cfg =  ConfigParser(interpolation=ExtendedInterpolation())
    try:
        cfg.read('./config.ini')
        cfg.sections()

        #cfgSet.api_key = str(cfg.get('Unity','api_key'))
        #cfgSet.seceret_key = str(cfg.get('Unity','seceret_key'))
        #cfgSet.passphrase = str(cfg.get('Unity','passphrase'))
        #log.info(cfgSet.api_key+","+cfgSet.seceret_key+","+cfgSet.passphrase)
        cfgSet.phoneKey = str(cfg.get('Unity','phoneKey'))
        log.info(cfgSet.phoneKey)

        cfgSet.phone = cfg.get('Unity','phone')
        log.info(str(cfgSet.phone))

        cfgSet.symbol1 = str(cfg.get('pair1','symbol'))
        cfgSet.priceHigh1 = cfg.getfloat('pair1','priceHigh')
        cfgSet.priceLow1 = cfg.getfloat('pair1','priceLow')
        log.info("pair1: "+str(cfgSet.symbol1)+" "+str(cfgSet.priceHigh1)+" "+str(cfgSet.priceLow1))
        print(("pair1: "+str(cfgSet.symbol1)+" "+str(cfgSet.priceHigh1)+" "+str(cfgSet.priceLow1)))

        cfgSet.symbol2 = str(cfg.get('pair2','symbol'))
        cfgSet.priceHigh2 = cfg.getfloat('pair2','priceHigh')
        cfgSet.priceLow2 = cfg.getfloat('pair2','priceLow')
        log.info("pair2: "+str(cfgSet.symbol2)+" "+str(cfgSet.priceHigh2)+" "+str(cfgSet.priceLow2 ))
       
        cfgSet.symbol3 = str(cfg.get('pair3','symbol'))
        cfgSet.priceHigh3 = cfg.getfloat('pair3','priceHigh')
        cfgSet.priceLow3 = cfg.getfloat('pair3','priceLow')
        log.info("pair3: "+str(cfgSet.symbol3)+" "+str(cfgSet.priceHigh3)+" "+str(cfgSet.priceLow3))
       
        cfgSet.symbol4 = str(cfg.get('pair4','symbol'))
        cfgSet.priceHigh4 = cfg.getfloat('pair4','priceHigh')
        cfgSet.priceLow4 = cfg.getfloat('pair4','priceLow')
        log.info("pair4: "+str(cfgSet.symbol4)+" "+str(cfgSet.priceHigh4)+" "+str(cfgSet.priceLow4))
       
    except Exception as e:
        log.error("config error ",str(e))
        print("config error ",str(e))

def on_message(ws, message):  # 服务器有数据更新时，主动推送过来的数据
    info = json.loads(message)
    if "event" in info:
        if info["event"] == "error":
            log.error(info)
            return
        elif info["event"] == "subscribe":
            log.info(info)
            return 

    ticker = info
    log.info(info)
    if 'data' not in ticker:
        log.info(info)
        return

    dataCheck(ticker['data'][0]['instId'],ticker['data'][0])
    #log.info(ticker['data'][i]['timestamp'])

def on_error(ws, error):  # 程序报错时，就会触发on_error事件
    log.error("on_error",str(error))

def on_close(ws):
    log.info("Connection closed ……")
    print("Connection closed ……")
    time.sleep(60)
    log.info("Connection restart!")
    webSocketRun()

def on_open(ws):  # 连接到服务器之后就会触发on_open事件，这里用于send数据
    # loginParams(ws)
    # time.sleep(2)
    sub_param = {"op": "subscribe", 
                 "args":[
                     {"channel":"tickers","instId":cfgSet.symbol1},
                     {"channel":"tickers","instId":cfgSet.symbol2},
                     {"channel":"tickers","instId":cfgSet.symbol3},
                     {"channel":"tickers","instId":cfgSet.symbol4}
                    ]
                }
    sub_str = json.dumps(sub_param)
    ws.send(sub_str)

# check time ,check price 
def dataCheck(symbol,data):

    try:
        lastPrice = float(data["last"])
    except Exception as e:
        print("error ",str(e))
        log.info("error ",str(e))

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
        log.info("error symbol:",symbol)
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
        log.error("config error ",str(e))
        result = {
            'error': -99999
        }
        json_str = json.dumps(result)
        print(json_str)
    print("call "+cfgSet.phone+" :"+warnInfo)
    log.info("call "+cfgSet.phone+" :"+warnInfo)
    log.info(result)
    print(result)
    return result

def webSocketRun():
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=15)
    log.info("webSocketRun ....")

if __name__ == "__main__":
    websocket.enableTrace(True)
    quoteWatchInit()
    webSocketRun()
