from ib_insync import *

# ✅ Connect to IB
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# ✅ Fetch daily historical data
contract = Stock('AAPL', 'SMART', 'USD')
bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='1 Y',
    barSizeSetting='1 day', whatToShow='ADJUSTED_LAST', useRTH=True)

# Convert to DataFrame
import pandas as pd
df = pd.DataFrame(bars)
print(df.head())  # ✅ Check if data is retrieved

