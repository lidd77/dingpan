#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests;
import json;
#import configparser
from configparser import ConfigParser,ExtendedInterpolation
# import websocket
import hmac
import base64
import zlib
from datetime import datetime

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time

#log config
import logging

import unittest
from huobi import *
from huobi.impl.websocketrequestimpl import WebsocketRequestImpl
from huobi.model import *
from huobi.impl.utils import *
from huobi.model import *

from pandas import  Series,DataFrame
import pandas as pd

import numpy as np
# import talib
import ta


# from tests.mock_websocket_connection import MockWebsocketConnection
from huobi.impl.utils.timeservice import convert_cst_in_millisecond_to_utc

# REST API
# https://api.huobi.pro
# Websocket Feed（行情）
# wss://api.huobi.pro/ws

# Websocket Feed（资产和订单）
# wss://api.huobi.pro/ws/v1


url = 'wss://api.huobi.pro/ws'
acessKey =   '47336ebb-db083389-vf25treb80-ef994'
SecretKey = '467db9e7-9228ac9d-3e31942a-6f89b'
logger = logging.getLogger("huobi-client")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)



def init():
    sub_client = SubscriptionClient(api_key=acessKey, secret_key=SecretKey,url = "https://api.huobi.vn")

def callback(candlestick_event: 'CandlestickEvent'):
    # print("Symbol: " + candlestick_event.symbol)
    # candlestick_event.data.print_object()
    print(candlestick_event.__dict__)
    print(candlestick_event.data.__dict__)
    # logger.info(candlestick_event)

def subscribe30mKline():
    sub_client.subscribe_candlestick_event("btcusdt", CandlestickInterval.MIN30, callback, error)
    
def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

# APScheduler
def addk30Task():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)
    scheduler.start()

def req30mKline():
    request_client = RequestClient(api_key=acessKey, secret_key=SecretKey)

    candlestick_list = request_client.get_latest_candlestick("btcusdt", CandlestickInterval.MIN1, 26)
    
    print("---- 1 min candlestick for btcusdt ----")
    print(candlestick_list)
    List26 = []
    for item in candlestick_list:
        #item.print_object()
        #print(item.close)
        #List26[i] = item.close
        List26.append(item.close)
        """
        print("Timestamp: " + str(item.timestamp))
        print("High: " + str(item.high))
        print("Low: " + str(item.low))
        print("Open: " + str(item.open))
        print("Close: " + str(item.close))
        print("Volume: " + str(item.volume))
        """
    print(List26)
    prices = np.array(List26)
    #macd_tmp = talib.MACD(prices, fastperiod=fast_period, slowperiod=slow_period, signalperiod=macd_window)
    macd_tmp = ta.trend.macd(prices,n_fast=12, n_slow=26, fillna=False)
    print(macd_tmp)

url1 =  "https://api.huobi.pro/market/history/kline?period=30min&size=30&symbol=btcusdt"
def req30mKline2():
    r = requests.get(url1)
    dataDict = json.loads(r.text)
    print(dataDict)
    dataList  = dataDict.get("data");
    print(dataList)
    print(type(dataList))
    
    List26 = []
    i = 0 
    dataLen = len(dataList)
    if dataLen >= 26:
        for item in dataList:
            i = i+1
            List26[i] = item["close"]
            print(item["close"])
            if  i >= 26:
                break
            

    print(List26)
    #testArray = "["+dataArray.text+"]"
    #print(testArray)
    # dataJson = json.loads(dataList)
    # print(dataList[1])
    prices = np.array(List26)

    # array = np.array(dataList)
    # print(type(array))
    # 周期快速移动平均
    fast_period = 12
    # 周期慢速移动平均
    slow_period = 26
    # 周期移动平均
    macd_window = 9
    # 历史数据要足够长，才能够拿到收敛的MACD
    # longest_history = 100

    #pd.read_json(dataArray,orient='records')
    #print(pd.read_json(array,orient='records'))
    #print(s.values)

    macd_tmp = talib.MACD(prices, fastperiod=fast_period, slowperiod=slow_period, signalperiod=macd_window)

    print(macd_tmp)

if __name__ == "__main__":
    req30mKline()
