# fetch_and_trade.py
import pandas as pd
import backtrader as bt
from ib_insync import *

# ---- Setup IB connection ----
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Make sure IB Gateway or TWS is running

# ---- Fetch historical data from IB ----
contract = Stock('AAPL', 'SMART', 'USD')

bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='1 Y',
    barSizeSetting='1 day',
    whatToShow='ADJUSTED_LAST',
    useRTH=True,
    formatDate=1
)

# Convert to DataFrame for easier handling
df = pd.DataFrame(bars)
df['datetime'] = pd.to_datetime(df['date'])
df.set_index('datetime', inplace=True)
df.drop(columns=['date'], inplace=True)

# ---- Define Backtrader Strategy ----
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy(size=10)
        elif self.data.close[0] < self.sma[0]:
            self.sell(size=10)

    def log(self, txt):
        dt = self.datas[0].datetime.datetime(0)
        print(f'{dt}: {txt}')

    def notify_order(self, order):
        if order.status in [order.Completed]:
            action = 'BUY' if order.isbuy() else 'SELL'
            self.log(f'{action} EXECUTED at {order.executed.price}')

# ---- Feed DataFrame into Backtrader ----
class PandasData(bt.feeds.PandasData):
    # PandasData automatically maps open, high, low, close, volume, and openinterest
    pass

# ---- Run Backtrader ----
cerebro = bt.Cerebro()
data = PandasData(dataname=df)
cerebro.adddata(data)
cerebro.addstrategy(MyStrategy)

cerebro.run()

# ---- Optional: Plot the result ----
cerebro.plot()
