# !/usr/bin/env python
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

import numpy as np
import talib
import KLineNum

from pandas import  Series,DataFrame
import pandas as pd


# 策略代码总共分为三大部分，1)PARAMS变量 2)initialize函数 3)handle_data函数
# 请根据指示阅读。或者直接点击运行回测按钮，进行测试，查看策略效果。

# 策略名称：MACD指标策略
# 策略详细介绍：https://wequant.io/study/strategy.macd.html
# 关键词：指数平滑移动均线、多空头预测。
# 方法：
# 1)利用talib库计算MACD值
# 2)MACD柱>0时买入，MACD柱<0时卖出


# 公式总结如下（以日为单位举例）：
# （1）计算快（12日）、慢（26日）两条EMA线：
#      EMA（12）=  前一日EMA（12）X 11/13 + 今日收盘价 X 2/13
#      EMA（26） =  前一日EMA（26）X 25/27 + 今日收盘价 X 2/27
# （2）计算离差值DIFF
#      DIFF = EMA（12）- EMA（26）
# （3）计算DIFF的EMA（9日）值DEA：
#    DEA = 前一日DEA X 8/10 + 今日DIF X 2/10

# （4）计算MACD：
#    MACD = （DIFF - DEA）* 2


# EMA(12)    //最近12 period 收盘价平均数
# EMA(26)   //最近26 period 的收盘价平均数
# EMA(9)     //最近9 period 的收盘价平均数

# DIFF

# DEA()
# DIF    //离差率

m30 = KLineNum.K30Min

aEMA12m30 = [m30(),m30(),m30(),m30(),m30(),
m30(),m30(),m30(),m30(),m30(),
m30(),m30()]
pEMA12m30 = 0;

aEMA26m30  = [m30(),m30(),m30(),m30(),m30(),
m30(),m30(),m30(),m30(),m30(),
m30(),m30(),m30(),m30(),m30(),
m30(),m30(),m30(),m30(),m30(),
m30(),m30(),m30(),m30(),m30(),
m30()]
pEMA26m30 = 0;

aEMA9m30 = [m30(),m30(),m30(),m30(),m30(),
m30(),m30(),m30(),m30(),m30(),
m30(),m30()]
pEMA9m30 = 0;

# sql_cmd='select * from XXXX'#输入你的SQL语句
# connection = mysql.connect(host='数据库IP',port="数据库端口",user='登录账户',password='登录密码',db='具体连接的库',charset='utf8')#创建数据库链接属性
# data = pd.read_sql(sql=sql_cmd,con=connection)#导入数据库查结果为DataFrame

def getDataFromSQL():
  pd.read_sql(query, connection_object) #从SQL表/库导入数据
  pd.read_json(json_string)  #从JSON格式的字符串导入数据

def getEMA12Value():
  sum = 0.0
  for  i in  range( len(aEMA12m30)):
    sum = aEMA12m30[i].close + sum
  average12 = sum/12.0
  return average12

def getEMA26Value():
  sum = 0.0
  for  i in  range( len(aEMA12m30)):
    sum = aEMA26m30[i].close + sum
  average26 = sum/26.0
  return average26

def getEMA9Value():
  sum = 0.0
  for  i in  range( len(aEMA12m30)):
    sum = aEMA9m30[i].close + sum
  average9 = sum/9.0
  return average9

def saveEMA12Value(newK30m):
  if pEMA12m30  >= 12:
    pEMA12m30 = 0
  aEMA12m30[pEMA12m30] =newK30m
  pEMA12m30 = pEMA12m30 + 1

def saveEMA26Value(newK30m):
  if pEMA26m30  >= 26:
    pEMA26m30 = 0
  aEMA26m30[pEMA26m30] = newK30m
  pEMA26m30 = pEMA26m30 + 1

def saveEMA9Value(newK30m):
  if pEMA9m30  >= 12:
    pEMA9m30 = 0
  aEMA9m30[pEMA9m30] = newK30m
  pEMA9m30 = pEMA9m30 + 1

def logInit():
    LOG_FORMAT = "%(asctime)s- %(levelname)s - %(message)s [%(filename)s:%(lineno)s]"
    filename = datetime.now().strftime("%Y%m%d-%H%M%S")+'.log'
    logging.basicConfig(filename="./logs/"+filename, level=logging.INFO, format=LOG_FORMAT)
    print("create ./logs/",filename)

def getQuoteK30min():
  pass
  # huobi
  # url =  "https://api.huobi.pro/market/history/kline?period=30min&size=200&symbol=btcusdt"
  # wss = "wss://api.huobi.pro/ws"
#  {  "sub": "market.ethbtc.kline.1min",  "id": "id1"}
#okex
#url = "spot/candle1800s"  # 30分钟k线数据频道
# {"op": "subscribe", "args": ["spot/candle60s:BTC-USDT","spot/candle60s:BCH-USDT","spot/candle60s:ETH-USDT","spot/candle60s:EOS-USDT"]}
# BTC-USDT  BCH-USDT ETH-UDST EOS-USDT 

# 阅读1，首次阅读可跳过:
# PARAMS用于设定程序参数，回测的起始时间、结束时间、滑点误差、初始资金和持仓。
# 可以仿照格式修改，基本都能运行。如果想了解详情请参考新手学堂的API文档。
PARAMS = {
    "start_time": "2017-02-01 00:00:00",
    "end_time": "2017-08-01 00:00:00",
    "slippage": 0.003,  # 此处“slippage"包含佣金（千二）+交易滑点（千一）
    "account_initial": {"huobi_cny_cash": 100000,
                      "huobi_cny_btc": 0},
}

# 阅读2，遇到不明白的变量可以跳过，需要的时候回来查阅:
# initialize函数是两大核心函数之一（另一个是handle_data），用于初始化策略变量。
# 策略变量包含：必填变量，以及非必填（用户自己方便使用）的变量
def initialize(context):
    # 设置回测频率, 可选："1m", "5m", "15m", "30m", "60m", "4h", "1d", "1w"
    context.frequency = "15m"
    # 设置回测基准, 比特币："huobi_cny_btc", 莱特币："huobi_cny_ltc", 以太坊："huobi_cny_eth"
    context.benchmark = "huobi_cny_btc"
    # 设置回测标的, 比特币："huobi_cny_btc", 莱特币："huobi_cny_ltc", 以太坊："huobi_cny_eth"
    context.security = "huobi_cny_btc"

    # 设置使用talib计算MACD的参数
    # 周期快速移动平均
    context.user_data.fast_period = 12
    # 周期慢速移动平均
    context.user_data.slow_period = 26
    # 周期移动平均
    context.user_data.macd_window = 9
    # 历史数据要足够长，才能够拿到收敛的MACD
    context.user_data.longest_history = 100

# 阅读3，策略核心逻辑：
# handle_data函数定义了策略的执行逻辑，按照frequency生成的bar依次读取并执行策略逻辑，直至程序结束。
# handle_data和bar的详细说明，请参考新手学堂的解释文档。
def handle_data(context):
    # 获取历史数据, 取后longest_history根bar
    hist = context.data.get_price(context.security, count=context.user_data.longest_history, frequency=context.frequency)
    if len(hist.index) < context.user_data.longest_history:
        context.log.warn("bar的数量不足, 等待下一根bar...")
        return

    # 历史收盘价
    prices = np.array(hist["close"])
    # 初始化买入卖出信号
    long_signal_triggered = False
    short_signal_triggered = False

    try:
        # talib计算MACD，返回三个数组，分别为DIF, DEA和MACD的值
        macd_tmp = talib.MACD(prices, fastperiod=context.user_data.fast_period, slowperiod=context.user_data.slow_period, signalperiod=context.user_data.macd_window)
        # 获取MACD值
        macd_hist = macd_tmp[2]
        # 获取最新一个MACD的值
        macd = macd_hist[-1]
        context.log.info("当前MACD为: %s" % macd)
    except:
        context.log.error("计算MACD出错...")
        return

    # macd大于0时，产生买入信号
    if macd > 0:
        long_signal_triggered = True
    # macd小于0时，产生卖出信号
    elif macd < 0:
        short_signal_triggered = True

    # 有卖出信号，且持有仓位，则市价单全仓卖出
    if short_signal_triggered:
        context.log.info("MACD小于0，产生卖出信号")
        if context.account.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY:
            # 卖出信号，且不是空仓，则市价单全仓清空
            context.log.info("正在卖出 %s" % context.security)
            context.log.info("卖出数量为 %s" % context.account.huobi_cny_btc)
            context.order.sell_limit(context.security, quantity=str(context.account.huobi_cny_btc), price=str(prices[-1]*0.98))
        else:
            context.log.info("仓位不足，无法卖出")
    # 有买入信号，且持有现金，则市价单全仓买入
    elif long_signal_triggered:
        context.log.info("MACD大于0，产生买入信号")
        if context.account.huobi_cny_cash >= HUOBI_CNY_BTC_MIN_ORDER_CASH_AMOUNT:
            # 买入信号，且持有现金，则市价单全仓买入
            context.log.info("正在买入 %s" % context.security)
            context.log.info("下单金额为 %s 元" % context.account.huobi_cny_cash)
            context.order.buy_limit(context.security, quantity=str(context.account.huobi_cny_cash/prices[-1]*0.98), price=str(prices[-1]*1.02))
        else:
            context.log.info("现金不足，无法下单")
    else:
        context.log.info("无交易信号，进入下一根bar")

url = 'wss://real.okex.com:10442/ws/v3'
#spot/candle1800s 
class cfgSet:
    pass

cfgSet = cfgSet()

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

def on_message(ws, message):  # 服务器有数据更新时，主动推送过来的数据
    decompress = zlib.decompressobj(-zlib.MAX_WBITS) # see above
    inflated = decompress.decompress(message)
    inflated += decompress.flush()
    data = str(inflated,encoding='utf-8')
    ticker = json.loads(data)
    logging.info(ticker)
    print(ticker)

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
    #sub_param = {"op": "subscribe", "args":[cfgSet.subscribe,cfgSet.kline_subscribe]}
    #sub_param = {"op": "subscribe", "args":["spot/candle1800s:BTC-USDT","spot/candle1800s:BCH-USDT","spot/candle1800s:ETH-USDT","spot/candle1800s:EOS-USDT"]}
    sub_param = {"op": "subscribe", "args":["spot/candle1800s:BTC-USDT"]}
    sub_str = json.dumps(sub_param)
    ws.send(sub_str)

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
    websocket.enableTrace(True)
    logInit()
    quoteWatchInit()
    webSocketRun()