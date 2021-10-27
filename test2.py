import pyupbit
from upbitpy import Upbitpy

access_key = "0bRrps8yJa7NolmhKI11vdT0RnBCVpDFzvjjo8e4"
secret_key = "5wasE2xSxPU5vrLmAfPYU8pfWNyhHi5yCu2c0ENu"
upbit = pyupbit.Upbit(access_key, secret_key)

ticker = "KRW-ATOM"

df = pyupbit.get_ohlcv(ticker, interval="minute1",count=2)


upbit = Upbitpy()
print(upbit.get_minutes_candles(1, ticker, count=1))
