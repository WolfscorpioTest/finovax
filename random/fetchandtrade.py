from backtrader_ib import ibstore

cerebro = bt.Cerebro()

# Set up IB store
store = ibstore.IBStore(host='127.0.0.1', port=7497, clientId=1)  # paper trading port is 7497
cerebro.broker = store.getbroker()

# Example data feed (daily data for AAPL)
data = store.getdata(dataname='AAPL', timeframe=bt.TimeFrame.Days, compression=1)

cerebro.adddata(data)

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma_short = bt.indicators.SMA(self.data.close, period=10)
        self.sma_long = bt.indicators.SMA(self.data.close, period=50)

    def next(self):
        if self.sma_short[0] > self.sma_long[0] and not self.position:
            self.buy()
        elif self.sma_short[0] < self.sma_long[0] and self.position:
            self.sell()
data = store.getdata(dataname='AAPL', timeframe=bt.TimeFrame.Days, compression=1)
cerebro.adddata(data)
def notify_order(self, order):
    if order.status in [order.Completed]:
        if order.isbuy():
            print(f'BUY EXECUTED: {order.executed.price}')
        elif order.issell():
            print(f'SELL EXECUTED: {order.executed.price}')
    elif order.status in [order.Canceled, order.Margin, order.Rejected]:
        print(f'Order Canceled/Margin/Rejected')
