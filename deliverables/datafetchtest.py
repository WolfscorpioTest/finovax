from ib_insync import *

def on_error(reqId, errorCode, errorString, _unused):
    print(f"⚠️ IB Error {errorCode}: {errorString}")

ib = IB()
ib.errorEvent += on_error  # Attach custom error handler

ib.connect('127.0.0.1', 7497, clientId=1)

contract = Stock('AAPL', 'SMART', 'USD')
ib.qualifyContracts(contract)

bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='1 W',  # Reduce duration to avoid overloading IB
    barSizeSetting='1 day',
    whatToShow='TRADES',
    useRTH=False,  # Ensure out-of-hours data is included
    formatDate=1
)

ib.waitOnUpdate(timeout=10)

if bars:
    print(f"✅ Retrieved {len(bars)} bars")
else:
    print("❌ No data received")
