import pyupbit
import time
from threading import Thread, Lock
from upbitpy import Upbitpy

access_key = 
secret_key = 
upbit = pyupbit.Upbit(access_key, secret_key)

lock=Lock()
class developer(Thread):
    def __init__(self,coin_name,cur_price):
        Thread.__init__(self)
        self.coin_name = coin_name
        self.state = 0
        self.cur_price = cur_price;
        self.buy_price = 0;
        self.sell_price = 0;
    def run(self):
        while 1:
            #orderbook = pyupbit.get_orderbook(self.coin_name)
            #total_ask_size_cur = orderbook[0]['total_ask_size']
            #total_bid_size_cur = orderbook[0]['total_bid_size']
            cur_price = pyupbit.get_current_price(self.coin_name)
            if cur_price == None:
                continue
            per = ((float(self.cur_price) - float(cur_price)) / float(self.cur_price)) * 100
            if per >= 3: #and total_ask_size_cur > total_bid_size_cur:
                print("+ " + str(self.coin_name) +" 처음 : " + str(self.cur_price) + " 나중 : " + str(cur_price));
            if per < -3:
                print("- " + str(self.coin_name) +" 처음 : " + str(self.cur_price) + " 나중 : " + str(cur_price));
            time.sleep(5)
            lock.acquire()
            lock.release()

# candle 요청 회수 제한이 걸리면 1초 sleep
def check_remaining_candles_req(upbit):
    ret = upbit.get_remaining_req()
    if ret is None:
        return
    if 'candles' not in ret.keys():
        return
    if int(ret['candles']['sec']) == 0:
        time.sleep(1)

upbit = Upbitpy()
tickers = pyupbit.get_tickers(fiat="KRW")
cur_prices = []
buy_prices = []
buy_num = []
buy_uuid = []
buy_check_list = [0 for i in range(len(tickers))]
candles_7d = dict()

for i in range(len(tickers)):
    ticker = tickers[i]
    buy_check_list[i] = 0
    cur_prices.append(pyupbit.get_current_price(ticker))
    buy_uuid.append("");
    buy_prices.append(0)
    buy_num.append(0)
    candles_7d[ticker] = upbit.get_weeks_candles(ticker, count=1)[0]
    check_remaining_candles_req(upbit)
    time.sleep(0.08)

while 1:
    for i in range(len(tickers)):
        ticker = tickers[i]
        if buy_check_list[i] == 0:
            cur_price = pyupbit.get_current_price(ticker)
            per = ((cur_price - cur_prices[i]) / cur_prices[i]) * 100
            if per >= 3:
                
                buy_num[i] = 1000.0 / cur_prices[i];
                #ret = upbit.buy_limit_order(ticker, cur_prices[i], buy_num[i])
                buy_uuid[i] = 0;#ret[0]['uuid']
                buy_prices[i] = cur_prices[i]
                buy_check_list[i] = 1
                print("+ " + ticker +" 산 가격 : " + str(cur_prices[i]) + " 오른가격 : " + str(cur_price) + "갯수 : "+ str(buy_num[i]))
            elif per < -3:
                cur_prices[i] = cur_price
        else:
            cur_price = pyupbit.get_current_price(ticker)
            per = ((cur_price - buy_prices[i]) / cur_prices[i]) * 100
            if per >= 3:
                cur_prices[i] = cur_price
                buy_check_list[i] = 0
                #ret = upbit.sell_limit_order(ticker, buy_prices[i], buy_num[i])
                #if 'error' in ret[0]:
                    #upbit.cancel_order(buy_uuid[i])
                #    print("이득인데 못삼 " + ticker +" 산 가격 : " + str(buy_prices[i]) + " 판 가격 : " + str(cur_price))
                #else:
                print("이득 " + ticker +" 산 가격 : " + str(buy_prices[i]) + " 판 가격 : " + str(cur_price))
            elif per < -3:
                cur_prices[i] = cur_price
                buy_check_list[i] = 0
                #ret = upbit.sell_limit_order(ticker, buy_prices[i], buy_num[i])
                #if 'error' in ret[0]:
                    #upbit.cancel_order(buy_uuid[i])
                #    print("손해인데 못삼 " + ticker +" 산 가격 : " + str(buy_prices[i]) + " 판 가격 : " + str(cur_price))
                #else:
                print("손해 " + ticker +" 산 가격 : " + str(buy_prices[i]) + " 판 가격 : " + str(cur_price))
    time.sleep(0.08)

ticker_thread_list=[]
for ticker in tickers:
    ticker_thread=developer(ticker, pyupbit.get_current_price(ticker))
    ticker_thread_list.append(ticker_thread)
    ticker_thread.start()
    time.sleep(1)

for ticker_thread in ticker_thread_list:
    ticker_thread.join()


    
