from ib_insync import *

def on_error(reqId, errorCode, errorString, _unused):
    print(f"⚠️ IB Error {errorCode}: {errorString}")

ib = IB()
ib.errorEvent += on_error  # Attach custom error handler

ib.connect('127.0.0.1', 7497, clientId=1)

contract = Stock('AAPL', 'SMART', 'USD')

bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='1 D',
    barSizeSetting='1 day',
    whatToShow='MIDPOINT',  # Adjust as needed: 'TRADES', 'BID', 'ASK'
    useRTH=False  # ✅ Get extended-hours data (pre-market, after-hours)
)

print(f"Received {len(bars)} bars")
