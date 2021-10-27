import pyupbit
from upbitpy import Upbitpy

access_key = 
secret_key = 
upbit = pyupbit.Upbit(access_key, secret_key)

ticker = "KRW-ATOM"

df = pyupbit.get_ohlcv(ticker, interval="minute1",count=2)


upbit = Upbitpy()
print(upbit.get_minutes_candles(1, ticker, count=1))
