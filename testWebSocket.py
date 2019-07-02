#!/usr/bin/env python

import asyncio
import websockets
import websocket
import json
import requests
import dateutil.parser as dp
import hmac
import base64
import zlib

api_key = '78e83f11-0fc6-41ba-bb60-8c9042dae10f'
seceret_key = '9F9E3F62F577C6C34FD73540044C4B15'
passphrase = '857824'
url = 'wss://real.okex.com:10442/ws/v3'
channels = ["swap/ticker:BTC-USD-SWAP"]
channel2 = ["spot/ticker:BTC-USDT","spot/ticker:ETH-USDT","spot/ticker:EOS-USDT"]

rst = asyncio.get_event_loop().run_until_complete(login(url, api_key, passphrase, seceret_key))

symbol1LastCallTime  = 0.0 
symbol2LastCallTime  = 0.0 
symbol3LastCallTime  = 0.0 

nowtime = time.time()
global symbol1LastCallTime,symbol2LastCallTime,symbol3LastCallTime



if symbol == cfgSet.symbol1:
    if nowtime - coin1LastCallTime < 3600*2:
        return 
    else:
        lastCallTime = nowtime
elif symbol == cfgSet.symbol2:
 
elif:


def login():
    unixTime = time.time()
    timestamp = str(round(unixTime))
    #login_str = login_params(str(timestamp), api_key, passphrase, secret_key)
    message = timestamp + 'GET' + '/users/self/verify'
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    sign = base64.b64encode(d)
    login_param = {"op": "login", "args": [api_key, passphrase, timestamp, sign.decode("utf-8")]}
    login_str = json.dumps(login_param)
    await websocket.send(login_str)
    login_res = await websocket.recv()

def login_params(timestamp, api_key, passphrase, secret_key):
    message = timestamp + 'GET' + '/users/self/verify'
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    sign = base64.b64encode(d)

    login_param = {"op": "login", "args": [api_key, passphrase, timestamp, sign.decode("utf-8")]}
    login_str = json.dumps(login_param)
    return login_str

'''
# subscribe channel without login
#
# swap/ticker // 行情数据频道
# swap/candle60s // 1分钟k线数据频道
# swap/candle180s // 3分钟k线数据频道
# swap/candle300s // 5分钟k线数据频道
# swap/candle900s // 15分钟k线数据频道
# swap/candle1800s // 30分钟k线数据频道
# swap/candle3600s // 1小时k线数据频道
# swap/candle7200s // 2小时k线数据频道
# swap/candle14400s // 4小时k线数据频道
# swap/candle21600 // 6小时k线数据频道
# swap/candle43200s // 12小时k线数据频道
# swap/candle86400s // 1day k线数据频道
# swap/candle604800s // 1week k线数据频道
# swap/trade // 交易信息频道
# swap/funding_rate//资金费率频道
# swap/price_range//限价范围频道
# swap/depth //深度数据频道，首次200档，后续增量
# swap/depth5 //深度数据频道，每次返回前5档
# swap/mark_price// 标记价格频道
async def subscribe_without_login(url, channels):
    async with websockets.connect(url) as websocket:
        sub_param = {"op": "subscribe", "args": channels}
        sub_str = json.dumps(sub_param)
        await  websocket.send(sub_str)
        print(f"send: {sub_str}")

        print("receive:")
        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")

        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")

# subscribe channel need login
#
# swap/account //用户账户信息频道
# swap/position //用户持仓信息频道
# swap/order //用户交易数据频道
async def subscribe(url, api_key, passphrase, secret_key, channels):
    async with websockets.connect(url) as websocket:
        # login
        timestamp = str(server_timestamp())
        login_str = login_params(str(timestamp), api_key, passphrase, secret_key)
        await websocket.send(login_str)

        login_res = await websocket.recv()
        # print(f"receive < {login_res}")

        sub_param = {"op": "subscribe", "args": channels}
        sub_str = json.dumps(sub_param)
        await  websocket.send(sub_str)
        print(f"send: {sub_str}")

        print("receive:")
        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")

        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")

# unsubscribe channels
async def unsubscribe(url, api_key, passphrase, secret_key, channels):
    async with websockets.connect(url) as websocket:
        timestamp = str(server_timestamp())

        login_str = login_params(str(timestamp), api_key, passphrase, secret_key)

        await websocket.send(login_str)

        greeting = await websocket.recv()
        # print(f"receive < {greeting}")

        sub_param = {"op": "unsubscribe", "args": channels}
        sub_str = json.dumps(sub_param)
        await  websocket.send(sub_str)
        print(f"send: {sub_str}")

        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")

# unsubscribe channels
async def unsubscribe_without_login(url, channels):
    async with websockets.connect(url) as websocket:
        sub_param = {"op": "unsubscribe", "args": channels}
        sub_str = json.dumps(sub_param)
        await  websocket.send(sub_str)
        print(f"send: {sub_str}")

        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")


url = 'wss://real.okex.com:10442/ws/v3'
# asyncio.get_event_loop().run_until_complete(login(url, api_key, passphrase, seceret_key))
channels = ["swap/ticker:BTC-USD-SWAP"]
# asyncio.get_event_loop().run_until_complete(subscribe(url, api_key, passphrase, seceret_key, channels))
# asyncio.get_event_loop().run_until_complete(unsubscribe(url, api_key, passphrase, seceret_key, channels))
asyncio.get_event_loop().run_until_complete(subscribe_without_login(url, channels))
#asyncio.get_event_loop().run_until_complete(unsubscribe_without_login(url, channels))

'''
def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

def on_message(ws, message):  # 服务器有数据更新时，主动推送过来的数据
    res = inflate(message)
    print(res)


def on_error(ws, error):  # 程序报错时，就会触发on_error事件

    print(error)

def on_close(ws):
    print("Connection closed ……")

def on_open(ws):  # 连接到服务器之后就会触发on_open事件，这里用于send数据
    sub_param = {"op": "subscribe", "args": channel2}
    sub_str = json.dumps(sub_param)
    print(sub_str)
    ws.send(sub_str)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=30)


'''
import json
from ws4py.client.threadedclient import WebSocketClient


class CG_Client(WebSocketClient):

    def opened(self):
        req = '{"event":"subscribe", "channel":"eth_usdt.deep"}'
        self.send(req)

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))
        data = resp['data']
        if type(data) is dict:
            ask = data['asks'][0]
            print('Ask:', ask)
            bid = data['bids'][0]
            print('Bid:', bid)


if __name__ == '__main__':
    ws = None
    try:
        ws = CG_Client('wss://i.cg.net/wi/ws')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
'''