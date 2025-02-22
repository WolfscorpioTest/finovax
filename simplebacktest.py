import backtrader as bt
import yfinance as yf
from datetime import datetime

class SmaCrossover(bt.Strategy):
    params = (("short_period", 10), ("long_period", 30),)

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(period=self.params.short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(period=self.params.long_period)

    def next(self):
        if self.sma_short[0] > self.sma_long[0] and self.sma_short[-1] <= self.sma_long[-1]:
            self.buy()
        elif self.sma_short[0] < self.sma_long[0] and self.sma_short[-1] >= self.sma_long[-1]:
            self.sell()

# ✅ Fetch data properly and check if a tuple is returned
data_tuple = yf.download('AAPL', start="2020-01-01", end="2023-01-01", progress=False)

# ✅ Check if we got a tuple and extract DataFrame
if isinstance(data_tuple, tuple):
    df = data_tuple[0]  # Extract the DataFrame from the tuple
else:
    df = data_tuple  # Use directly if it's already a DataFrame

# ✅ Check if DataFrame is empty
if df.empty:
    raise ValueError("No data downloaded. Check ticker symbol and internet connection.")

# ✅ Ensure correct column format for Backtrader
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]  # Use only required columns
df.columns = ["open", "high", "low", "close", "volume"]  # Rename to lowercase

# ✅ Convert to Backtrader data feed
data = bt.feeds.PandasData(dataname=df)

# Initialize Cerebro engine
cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCrossover)
cerebro.adddata(data)
cerebro.broker.set_cash(10000)  # Initial capital
cerebro.addsizer(bt.sizers.PercentSizer, percents=10)  # Risk 10% per trade
cerebro.run()
cerebro.plot()
